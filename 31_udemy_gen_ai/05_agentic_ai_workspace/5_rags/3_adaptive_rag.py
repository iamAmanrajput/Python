# Example of Adaptive Rag
import os
from typing import List, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


# ============================================================
# 1. Environment Setup
# ============================================================

# Load API keys and other environment variables from the .env file.
load_dotenv()

# Make sure the required API keys are available.
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is not set in the environment.")

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY is not set in the environment.")


# ============================================================
# 2. Load and Index Documents
# ============================================================

# Ollama creates embeddings for the documents stored in the vector store.
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Documents used as the knowledge source for the vector store.
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

# Load documents from all URLs.
loaded_documents = [WebBaseLoader(url).load() for url in urls]

# Flatten the nested list returned by the loaders.
documents = [
    document
    for document_group in loaded_documents
    for document in document_group
]

# Split documents into smaller chunks for better retrieval.
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500,
    chunk_overlap=0,
)

document_chunks = text_splitter.split_documents(documents)

# Store document chunks in FAISS using Ollama embeddings.
vectorstore = FAISS.from_documents(
    documents=document_chunks,
    embedding=embeddings,
)

# Create a retriever from the vector store.
retriever = vectorstore.as_retriever()


# ============================================================
# 3. LLM Setup
# ============================================================

# Groq LLM is used for routing, grading, query rewriting, and answer generation.
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
)


# ============================================================
# 4. Question Router
# ============================================================

class RouteQuery(BaseModel):
    """Route a user question to the most relevant data source."""

    datasource: Literal["vectorstore", "web_search"] = Field(
        description=(
            "Choose 'vectorstore' for questions about agents, prompt engineering, "
            "or adversarial attacks. Otherwise choose 'web_search'."
        )
    )


# Configure the LLM to return the RouteQuery structure.
structured_router = llm.with_structured_output(RouteQuery)

router_system_prompt = """You are an expert at routing a user question to a vectorstore or web search.

The vectorstore contains documents related to:
- AI agents
- Prompt engineering
- Adversarial attacks on LLMs

Use the vectorstore for questions related to these topics.
For all other questions, use web search.
"""

router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", router_system_prompt),
        ("human", "{question}"),
    ]
)

question_router = router_prompt | structured_router


# ============================================================
# 5. Document Relevance Grader
# ============================================================

class GradeDocuments(BaseModel):
    """Binary score for checking whether a retrieved document is relevant."""

    binary_score: Literal["yes", "no"] = Field(
        description="Return 'yes' if the document is relevant to the question, otherwise 'no'."
    )


# Configure the LLM to return the document grading structure.
structured_document_grader = llm.with_structured_output(GradeDocuments)

document_grader_system_prompt = """You are a grader assessing the relevance of a retrieved document to a user question.

If the document contains keywords, information, or semantic meaning related to the question,
grade it as relevant.

Return:
- 'yes' if the document is relevant
- 'no' if the document is not relevant
"""

document_grader_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", document_grader_system_prompt),
        (
            "human",
            "Retrieved document:\n\n{document}\n\n"
            "User question: {question}",
        ),
    ]
)

document_grader = document_grader_prompt | structured_document_grader


# ============================================================
# 6. RAG Generation Chain
# ============================================================

rag_system_prompt = """You are an assistant for question-answering tasks.

Use the retrieved context to answer the user's question.

If you do not know the answer from the provided context, say that you do not know.

Keep the answer concise and use a maximum of three sentences.
"""

rag_human_prompt = """Question: {question}

Context:
{context}

Answer:
"""

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        ("human", rag_human_prompt),
    ]
)


def format_documents(documents: List[Document]) -> str:
    """Convert retrieved Document objects into one text string."""
    return "\n\n".join(document.page_content for document in documents)


# Use a formatter before passing retrieved documents to the LLM.
rag_chain = (
    {
        "context": lambda state: format_documents(state["documents"]),
        "question": lambda state: state["question"],
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# 7. Hallucination Grader
# ============================================================

class GradeHallucinations(BaseModel):
    """Binary score for checking whether an answer is grounded in the context."""

    binary_score: Literal["yes", "no"] = Field(
        description="Return 'yes' if the answer is grounded in the provided facts, otherwise 'no'."
    )


structured_hallucination_grader = llm.with_structured_output(
    GradeHallucinations
)

hallucination_system_prompt = """You are a grader assessing whether an LLM-generated answer
is grounded in and supported by the provided retrieved facts.

Return:
- 'yes' if the answer is supported by the facts
- 'no' if the answer contains unsupported information
"""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", hallucination_system_prompt),
        (
            "human",
            "Retrieved facts:\n\n{documents}\n\n"
            "LLM generation:\n{generation}",
        ),
    ]
)

hallucination_grader = hallucination_prompt | structured_hallucination_grader


# ============================================================
# 8. Answer Grader
# ============================================================

class GradeAnswer(BaseModel):
    """Binary score for checking whether an answer addresses the question."""

    binary_score: Literal["yes", "no"] = Field(
        description="Return 'yes' if the answer addresses the question, otherwise 'no'."
    )


structured_answer_grader = llm.with_structured_output(GradeAnswer)

answer_grader_system_prompt = """You are a grader assessing whether an answer addresses and resolves
the user's question.

Return:
- 'yes' if the answer resolves the question
- 'no' if the answer does not resolve the question
"""

answer_grader_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", answer_grader_system_prompt),
        (
            "human",
            "User question:\n\n{question}\n\n"
            "LLM generation:\n{generation}",
        ),
    ]
)

answer_grader = answer_grader_prompt | structured_answer_grader


# ============================================================
# 9. Question Rewriter
# ============================================================

rewriter_system_prompt = """You are a question re-writer.

Convert the input question into a better version optimized for vectorstore retrieval.
Preserve the original intent while making the question more specific and semantically clear.
"""

rewriter_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewriter_system_prompt),
        (
            "human",
            "Here is the initial question:\n\n{question}\n\n"
            "Formulate an improved question.",
        ),
    ]
)

question_rewriter = rewriter_prompt | llm | StrOutputParser()


# ============================================================
# 10. Web Search Tool
# ============================================================

# Tavily is used when the question is outside the vectorstore's domain
# or when retrieved documents are not relevant.
web_search_tool = TavilySearchResults(k=3)


# ============================================================
# 11. LangGraph State
# ============================================================

class GraphState(TypedDict):
    """
    Represents the state passed between nodes in the Adaptive RAG graph.

    Attributes:
        question: Current user question.
        generation: Generated answer.
        documents: Retrieved documents used as context.
    """

    question: str
    generation: str
    documents: List[Document]


# ============================================================
# 12. Graph Nodes
# ============================================================

def retrieve(state: GraphState):
    """Retrieve relevant documents from the vector store."""
    print("\n--- RETRIEVE ---")

    question = state["question"]
    documents = retriever.invoke(question)

    return {
        "question": question,
        "documents": documents,
    }


def grade_documents(state: GraphState):
    """Filter retrieved documents and keep only relevant documents."""
    print("\n--- CHECK DOCUMENT RELEVANCE ---")

    question = state["question"]
    documents = state["documents"]

    filtered_documents = []

    for document in documents:
        score = document_grader.invoke(
            {
                "question": question,
                "document": document.page_content,
            }
        )

        if score.binary_score == "yes":
            print("--- GRADE: DOCUMENT RELEVANT ---")
            filtered_documents.append(document)
        else:
            print("--- GRADE: DOCUMENT NOT RELEVANT ---")

    return {
        "question": question,
        "documents": filtered_documents,
    }


def transform_query(state: GraphState):
    """Rewrite the question to improve vectorstore retrieval."""
    print("\n--- TRANSFORM QUERY ---")

    question = state["question"]
    documents = state["documents"]

    better_question = question_rewriter.invoke({"question": question})

    return {
        "question": better_question,
        "documents": documents,
    }


def web_search(state: GraphState):
    """Search the web and convert search results into Document objects."""
    print("\n--- WEB SEARCH ---")

    question = state["question"]
    search_results = web_search_tool.invoke({"query": question})

    web_documents = [
        Document(
            page_content=result.get("content", ""),
            metadata={"source": result.get("url", "")},
        )
        for result in search_results
        if result.get("content")
    ]

    return {
        "question": question,
        "documents": web_documents,
    }


def generate(state: GraphState):
    """Generate an answer using the retrieved documents."""
    print("\n--- GENERATE ---")

    question = state["question"]
    documents = state["documents"]

    generation = rag_chain.invoke(
        {
            "question": question,
            "documents": documents,
        }
    )

    return {
        "question": question,
        "documents": documents,
        "generation": generation,
    }


# ============================================================
# 13. Conditional Routing Functions
# ============================================================

def route_question(state: GraphState) -> str:
    """Route the question to either the vector store or web search."""
    print("\n--- ROUTE QUESTION ---")

    question = state["question"]
    route = question_router.invoke({"question": question})

    if route.datasource == "web_search":
        print("--- ROUTE: WEB SEARCH ---")
        return "web_search"

    print("--- ROUTE: VECTORSTORE ---")
    return "retrieve"


def decide_to_generate(state: GraphState) -> str:
    """
    Decide whether to generate an answer or rewrite the question.

    If no relevant documents remain after grading, the query is rewritten
    and sent back to retrieval.
    """
    print("\n--- ASSESS GRADED DOCUMENTS ---")

    if not state["documents"]:
        print("--- DECISION: TRANSFORM QUERY ---")
        return "transform_query"

    print("--- DECISION: GENERATE ---")
    return "generate"


def grade_generation(state: GraphState) -> str:
    """
    Check whether the generated answer is grounded in the documents
    and whether it answers the user's question.
    """
    print("\n--- CHECK HALLUCINATIONS ---")

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    hallucination_score = hallucination_grader.invoke(
        {
            "documents": format_documents(documents),
            "generation": generation,
        }
    )

    if hallucination_score.binary_score != "yes":
        print("--- DECISION: GENERATION NOT GROUNDED ---")
        return "not_supported"

    print("--- DECISION: GENERATION GROUNDED ---")
    print("--- CHECK ANSWER RELEVANCE ---")

    answer_score = answer_grader.invoke(
        {
            "question": question,
            "generation": generation,
        }
    )

    if answer_score.binary_score == "yes":
        print("--- DECISION: ANSWER IS USEFUL ---")
        return "useful"

    print("--- DECISION: ANSWER IS NOT USEFUL ---")
    return "not_useful"


# ============================================================
# 14. Build Adaptive RAG Workflow
# ============================================================

workflow = StateGraph(GraphState)

# Add graph nodes.
workflow.add_node("web_search", web_search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)

# Route the initial question.
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "web_search": "web_search",
        "retrieve": "retrieve",
    },
)

# Web search results go directly to generation.
workflow.add_edge("web_search", "generate")

# Vectorstore retrieval goes through document relevance grading.
workflow.add_edge("retrieve", "grade_documents")

# Decide whether relevant documents were found.
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)

# After rewriting the question, retrieve documents again.
workflow.add_edge("transform_query", "retrieve")

# After generation, check grounding and answer quality.
workflow.add_conditional_edges(
    "generate",
    grade_generation,
    {
        "not_supported": "transform_query",
        "useful": END,
        "not_useful": "transform_query",
    },
)


# Compile the graph.
app = workflow.compile()


# ============================================================
# 15. Run Adaptive RAG
# ============================================================

if __name__ == "__main__":
    result = app.invoke(
        {
            "question": "What is machine learning?",
            "documents": [],
            "generation": "",
        }
    )

    print("\n--- FINAL ANSWER ---")
    print(result["generation"])

# --- ROUTE QUESTION ---
# --- ROUTE: WEB SEARCH ---

# --- WEB SEARCH ---

# --- GENERATE ---

# --- CHECK HALLUCINATIONS ---
# --- DECISION: GENERATION GROUNDED ---
# --- CHECK ANSWER RELEVANCE ---
# --- DECISION: ANSWER IS USEFUL ---

# --- FINAL ANSWER ---

# Machine learning is a subfield of artificial intelligence focused on developing algorithms that learn patterns from data to make predictions or decisions without explicit programming. By training on datasets, these systems generalize their knowledge to perform tasks and continuously improve when exposed to new information. This data-driven approach now serves as the foundation for most modern AI applications.