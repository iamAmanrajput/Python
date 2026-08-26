# Example of Agentic Rag
import os
from dotenv import load_dotenv
import langchainhub as hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import create_retriever_tool
from typing import Annotated, Sequence, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Load environment variables from the .env file
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Create the Groq LLM
llm = ChatGroq(model="qwen/qwen3.6-27b")


# Create the embedding model using Ollama
# Make sure this model is available in your local Ollama setup
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# URLs containing LangGraph documentation
langgraph_urls = [
    "https://langchain-ai.github.io/langgraph/tutorials/introduction/",
    "https://langchain-ai.github.io/langgraph/tutorials/workflows/",
    "https://langchain-ai.github.io/langgraph/how-tos/map-reduce/"
]


# Load the content from each URL
# Each URL returns a list of Document objects
langgraph_docs = [
    WebBaseLoader(url).load()
    for url in langgraph_urls
]


# Flatten the nested list into a single list of Documents
langgraph_doc_list = [
    doc
    for sublist in langgraph_docs
    for doc in sublist
]


# Split the documents into smaller chunks
# chunk_size = maximum size of each chunk
# chunk_overlap = number of characters shared between consecutive chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

langgraph_splits = text_splitter.split_documents(langgraph_doc_list)


# Create a separate vector database for LangGraph documents
# The documents are converted into embeddings and stored in FAISS
langgraph_vectorstore = FAISS.from_documents(
    documents=langgraph_splits,
    embedding=embeddings
)


# Convert the vector database into a retriever
# The retriever finds relevant LangGraph documents for a query
langgraph_retriever = langgraph_vectorstore.as_retriever()


# Create a tool that allows the LLM/agent to search LangGraph documents
langgraph_retriever_tool = create_retriever_tool(
    langgraph_retriever,
    "retriever_vector_db_blog",
    "Search and retrieve information about LangGraph"
)


### LangChain Blogs - Separate Vector DB


# URLs containing LangChain documentation
langchain_urls = [
    "https://python.langchain.com/docs/tutorials/",
    "https://python.langchain.com/docs/tutorials/chatbot/",
    "https://python.langchain.com/docs/tutorials/qa_chat_history/"
]


# Load the content from each LangChain URL
langchain_docs = [
    WebBaseLoader(url).load()
    for url in langchain_urls
]


# Flatten the nested list into a single list of Documents
langchain_doc_list = [
    doc
    for sublist in langchain_docs
    for doc in sublist
]


# Split LangChain documents into smaller chunks
langchain_splits = text_splitter.split_documents(langchain_doc_list)


# Create a separate vector database for LangChain documents
langchain_vectorstore = FAISS.from_documents(
    documents=langchain_splits,
    embedding=embeddings
)


# Convert the LangChain vector database into a retriever
langchain_retriever = langchain_vectorstore.as_retriever()


# Create a tool that allows the LLM/agent to search LangChain documents
langchain_retriever_tool = create_retriever_tool(
    langchain_retriever,
    "retriever_vector_langchain_blog",
    "Search and retrieve information about LangChain"
)


# Store both retriever tools in a list
# The agent can choose the appropriate tool based on the user's query
tools = [
    langgraph_retriever_tool,
    langchain_retriever_tool
]

class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed.
    # Default is to replace. add_messages says "append".
    messages: Annotated[Sequence[BaseMessage], add_messages]

def agent(state):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")
    messages = state["messages"]
    model = ChatGroq(model="qwen/qwen3.6-27b")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

### Edges
def grade_documents(state) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM
    model = ChatGroq(model="qwen/qwen3.6-27b")

    # LLM with tool and validation
    llm_with_tool = model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "rewrite"


def generate(state):
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
        dict: The updated message
    """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # LLM
    llm = ChatGroq(model="qwen/qwen3.6-27b")

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}


def rewrite(state):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
    HumanMessage(
        content=f""" \
    Look at the input and try to reason about the underlying semantic intent / meaning. \
    Here is the initial question:
    \n ------- \n
    {question}
    \n ------- \n
    Formulate an improved question:""",
        )
    ]

    # Grader
    model = ChatGroq(model="qwen/qwen3.6-27b")
    response = model.invoke(msg)
    return {"messages": [HumanMessage(content=response.content)]}


# Define a new graph
workflow = StateGraph(AgentState)

# Define the nodes we will cycle between
workflow.add_node("agent", agent)  # agent
retrieve = ToolNode([langgraph_retriever_tool, langchain_retriever_tool])
workflow.add_node("retrieve", retrieve)  # retrieval
workflow.add_node("rewrite", rewrite)  # Re-writing the question
workflow.add_node(
    "generate", generate
)  # Generating a response after we know the documents are relevant

# Call agent node to decide to retrieve or not
workflow.add_edge(START, "agent")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "agent",
    # Assess agent decision
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

# Edges taken after the `action` node is called.
workflow.add_conditional_edges(
    "retrieve",
    # Assess agent decision
    grade_documents,
)
workflow.add_edge("generate", END)
workflow.add_edge("rewrite", "agent")

# Compile
graph = workflow.compile()

result=graph.invoke({"messages": "What is Machine Learning?"})

print(result["messages"][-1].content)

# ---CALL AGENT---
# Machine Learning (ML) is a subset of **Artificial Intelligence (AI)** that provides systems the ability to automaticallylearn and improve from experience without being explicitly programmed.

# In traditional programming, humans write specific rules and instructions for the computer to follow (e.g., "If X happens, do Y"). In Machine Learning, you provide the computer with a large amount of data and a goal, and the computer builds its own rules and models based on patterns it finds in that data.

# ### How It Works
# 1.  **Data**: The system is fed large datasets.
# 2.  **Training**: The algorithm analyzes the data to identify patterns and correlations.
# 3.  **Model**: The system creates a mathematical model based on what it learned.
# 4.  **Prediction**: The model is used to make predictions or decisions on new, unseen data.

# ### Main Types of Machine Learning
# *   **Supervised Learning**: The algorithm is trained on "labeled" data (data where the correct answer is already known). For example, teaching an email filter by showing it thousands of emails labeled as "spam" or "not spam."
# *   **Unsupervised Learning**: The algorithm is given data without labels and must find hidden structures or patterns onits own. For example, grouping customers by purchasing behavior without being told beforehand what the groups should be.
# *   **Reinforcement Learning**: The algorithm learns through trial and error. It receives rewards for correct actions and penalties for incorrect ones. This is often used in robotics or game playing (like AlphaGo).

# Machine Learning is the technology behind many modern applications, including facial recognition, self-driving cars, recommendation systems (like Netflix or Spotify), and Large Language Models (like the one you are talking to now).