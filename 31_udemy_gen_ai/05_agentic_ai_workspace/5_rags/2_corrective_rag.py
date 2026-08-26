# Example of Corrective Rag
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import START, END, StateGraph


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")


# ============================================================
# 2. Create embedding model
# ============================================================

# Ollama is used to create embeddings for the documents.
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# ============================================================
# 3. Load documents
# ============================================================

# Websites that we want to use as our knowledge source.
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

# Load documents from all URLs.
docs = [WebBaseLoader(url).load() for url in urls]

# Flatten the nested list of documents into a single list.
docs_list = [doc for sublist in docs for doc in sublist]


# ============================================================
# 4. Split documents into smaller chunks
# ============================================================

# Smaller chunks make retrieval more focused and efficient.
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500,
    chunk_overlap=0,
)

doc_splits = text_splitter.split_documents(docs_list)


# ============================================================
# 5. Create vector store and retriever
# ============================================================

# Store document chunks in FAISS using Ollama embeddings.
vectorstore = FAISS.from_documents(
    documents=doc_splits,
    embedding=embeddings,
)

# Create a retriever from the vector store.
retriever = vectorstore.as_retriever()


# ============================================================
# 6. Create LLM
# ============================================================

# Groq LLM is used for grading, query rewriting, and generation.
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
)


# ============================================================
# 7. Document relevance grader
# ============================================================

class GradeDocuments(BaseModel):
    """Score whether a retrieved document is relevant to the question."""

    binary_score: str = Field(
        description="Documents are relevant to the question: 'yes' or 'no'."
    )


# Use structured output so the LLM returns a fixed format.
structured_llm_grader = llm.with_structured_output(GradeDocuments)


# Prompt used to check document relevance.
grader_system_prompt = """
You are a grader assessing the relevance of a retrieved document
to a user question.

If the document contains keywords or semantic meaning related
to the question, grade it as relevant.

Return only a binary score:
'yes' if the document is relevant,
'no' if the document is not relevant.
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", grader_system_prompt),
        (
            "human",
            "Retrieved document:\n\n{document}\n\n"
            "User question: {question}",
        ),
    ]
)

# Create the document relevance grading chain.
retrieval_grader = grade_prompt | structured_llm_grader


# ============================================================
# 8. RAG prompt
# ============================================================

# Prompt used to generate the final answer from retrieved context.
rag_system_prompt = """
You are an assistant for question-answering tasks.

Use the following pieces of retrieved context to answer the question.

If you don't know the answer, just say that you don't know.

Use three sentences maximum and keep the answer concise.
"""

rag_human_prompt = """
Question: {question}

Context: {context}

Answer:
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        ("human", rag_human_prompt),
    ]
)


# ============================================================
# 9. Format documents
# ============================================================

def format_docs(documents: List[Document]) -> str:
    """Convert a list of Document objects into a single text string."""

    return "\n\n".join(
        document.page_content for document in documents
    )


# Create the RAG generation chain.
rag_chain = prompt | llm | StrOutputParser()


# ============================================================
# 10. Question re-writer
# ============================================================

# This prompt rewrites the question to make it better for web search.
rewrite_system_prompt = """
You are a question re-writer that converts an input question
into a better version optimized for web search.

Look at the input and reason about its underlying semantic
intent and meaning.
"""

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewrite_system_prompt),
        (
            "human",
            "Here is the initial question:\n\n"
            "{question}\n\n"
            "Formulate an improved question.",
        ),
    ]
)

# Create the question rewriting chain.
question_rewriter = rewrite_prompt | llm | StrOutputParser()


# ============================================================
# 11. Tavily web search tool
# ============================================================

# Tavily is used when the retrieved documents are not sufficient.
web_search_tool = TavilySearchResults(k=3)


# ============================================================
# 12. Define graph state
# ============================================================

class GraphState(TypedDict):
    """
    Represents the current state of the CRAG workflow.

    Attributes:
        question: Current user question.
        generation: Final LLM-generated answer.
        web_search: Whether web search is required.
        documents: Retrieved and processed documents.
    """

    question: str
    generation: str
    web_search: str
    documents: List[Document]


# ============================================================
# 13. Retrieve documents
# ============================================================

def retrieve(state: GraphState):
    """Retrieve relevant documents from the vector store."""

    print("\n--- RETRIEVE ---")

    question = state["question"]

    # Retrieve documents using the user's question.
    documents = retriever.invoke(question)

    return {
        "documents": documents,
        "question": question,
    }


# ============================================================
# 14. Grade retrieved documents
# ============================================================

def grade_documents(state: GraphState):
    """Check whether retrieved documents are relevant to the question."""

    print("\n--- CHECK DOCUMENT RELEVANCE ---")

    question = state["question"]
    documents = state["documents"]

    # Store only relevant documents.
    filtered_documents = []

    # By default, web search is not required.
    web_search = "No"

    # Grade every retrieved document.
    for document in documents:

        score = retrieval_grader.invoke(
            {
                "question": question,
                "document": document.page_content,
            }
        )

        grade = score.binary_score.lower().strip()

        if grade == "yes":
            print("--- GRADE: DOCUMENT RELEVANT ---")
            filtered_documents.append(document)

        else:
            print("--- GRADE: DOCUMENT NOT RELEVANT ---")
            web_search = "Yes"

    return {
        "documents": filtered_documents,
        "question": question,
        "web_search": web_search,
    }


# ============================================================
# 15. Generate answer
# ============================================================

def generate(state: GraphState):
    """Generate the final answer using the available documents."""

    print("\n--- GENERATE ---")

    question = state["question"]
    documents = state["documents"]

    # Convert Document objects into plain text context.
    context = format_docs(documents)

    # Generate the final answer using the RAG chain.
    generation = rag_chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return {
        "documents": documents,
        "question": question,
        "generation": generation,
    }


# ============================================================
# 16. Transform query
# ============================================================

def transform_query(state: GraphState):
    """Rewrite the question to make it better for web search."""

    print("\n--- TRANSFORM QUERY ---")

    question = state["question"]
    documents = state["documents"]

    # Rewrite the original question.
    better_question = question_rewriter.invoke(
        {"question": question}
    )

    print(f"Original question: {question}")
    print(f"Improved question: {better_question}")

    return {
        "documents": documents,
        "question": better_question,
    }


# ============================================================
# 17. Web search
# ============================================================

def web_search(state: GraphState):
    """Search the web using the rewritten question."""

    print("\n--- WEB SEARCH ---")

    question = state["question"]
    documents = state["documents"]

    # Search the web using Tavily.
    search_results = web_search_tool.invoke(
        {"query": question}
    )

    # Extract the content from each search result.
    web_results = "\n\n".join(
        result["content"] for result in search_results
    )

    # Convert web results into a Document object.
    web_document = Document(page_content=web_results)

    # Add web results to the existing documents.
    documents.append(web_document)

    return {
        "documents": documents,
        "question": question,
    }


# ============================================================
# 18. Decide next step
# ============================================================

def decide_to_generate(state: GraphState):
    """
    Decide whether to generate the answer or rewrite the question
    and perform a web search.
    """

    print("\n--- ASSESS GRADED DOCUMENTS ---")

    web_search_required = state["web_search"]

    if web_search_required == "Yes":

        print(
            "--- DECISION: DOCUMENTS NOT SUFFICIENT, "
            "TRANSFORM QUERY ---"
        )

        return "transform_query"

    else:

        print("--- DECISION: GENERATE ---")

        return "generate"


# ============================================================
# 19. Build the LangGraph workflow
# ============================================================

workflow = StateGraph(GraphState)


# ------------------------------------------------------------
# Define nodes
# ------------------------------------------------------------

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)
workflow.add_node("web_search", web_search)


# ------------------------------------------------------------
# Define edges
# ------------------------------------------------------------

# Start with document retrieval.
workflow.add_edge(START, "retrieve")

# After retrieval, grade the documents.
workflow.add_edge("retrieve", "grade_documents")

# Decide whether to generate or search the web.
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)

# After rewriting the question, perform web search.
workflow.add_edge("transform_query", "web_search")

# After web search, generate the final answer.
workflow.add_edge("web_search", "generate")

# End the workflow after generation.
workflow.add_edge("generate", END)


# ============================================================
# 20. Compile the graph
# ============================================================

app = workflow.compile()


# ============================================================
# 21. Run the CRAG application
# ============================================================

result = app.invoke(
    {
        "question": "What are the types of agent memory?"
    }
)

print("\n--- FINAL ANSWER ---")
print(result["generation"])


# --- RETRIEVE ---

# --- CHECK DOCUMENT RELEVANCE ---
# --- GRADE: DOCUMENT RELEVANT ---
# --- GRADE: DOCUMENT RELEVANT ---
# --- GRADE: DOCUMENT RELEVANT ---
# --- GRADE: DOCUMENT RELEVANT ---

# --- ASSESS GRADED DOCUMENTS ---
# --- DECISION: GENERATE ---

# --- GENERATE ---

# --- FINAL ANSWER ---

# Based on the provided context, agent memory is categorized into three main types: sensory memory, which learns embedding representations from raw inputs; short-term memory, which handles in-context learning within the model's finite context window; and long-term memory, which utilizes an external vector store to retain and retrieve information over extended periods.