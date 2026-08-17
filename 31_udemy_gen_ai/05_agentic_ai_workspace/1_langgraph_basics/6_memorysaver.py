# LangGraph Agent with MemorySaver

from dotenv import load_dotenv
import os

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AnyMessage

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from typing import Annotated
from typing_extensions import TypedDict


# Load environment variables
load_dotenv()


# Enable LangSmith tracing
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "ReAct-agent"


# ---------------------------------------------------------
# Custom Tools
# ---------------------------------------------------------

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    return a / b


# List of tools available to the LLM
tools = [add, multiply, divide]


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatOllama(model="qwen3.5:0.8b")

# Bind tools with the LLM
llm_with_tools = llm.bind_tools(tools)


# ---------------------------------------------------------
# Graph State
# ---------------------------------------------------------

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# ---------------------------------------------------------
# LLM Node
# ---------------------------------------------------------

def tool_calling_llm(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# ---------------------------------------------------------
# Build Graph
# ---------------------------------------------------------

builder = StateGraph(State)

# Add LLM node
builder.add_node("tool_calling_llm", tool_calling_llm)

# Add Tool node
builder.add_node(
    "tools",
    ToolNode(tools)
)

# START → LLM
builder.add_edge(START, "tool_calling_llm")

# LLM → Tools or END
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)

# Tools → LLM
builder.add_edge("tools", "tool_calling_llm")


# ---------------------------------------------------------
# Add Memory
# ---------------------------------------------------------

memory = MemorySaver()

# Compile graph with MemorySaver
graph = builder.compile(
    checkpointer=memory
)


# ---------------------------------------------------------
# Run Graph
# ---------------------------------------------------------

# Thread ID identifies a conversation/thread
config = {
    "configurable": {
        "thread_id": "1"
    }
}

messages = graph.invoke(
    {
        "messages": [
            HumanMessage(content="Add 12 and 13.")
        ]
    },
    config=config
)


# Print all messages
for message in messages["messages"]:
    message.pretty_print()

# ================================ Human Message =================================

# Add 12 and 13.
# ================================== Ai Message ==================================
# Tool Calls:
#   add (08b54a5c-da65-4ce5-b1b8-208e286f963e)
#  Call ID: 08b54a5c-da65-4ce5-b1b8-208e286f963e
#   Args:
#     a: 12
#     b: 13
# ================================= Tool Message =================================
# Name: add

# 25
# ================================== Ai Message ==================================

# The sum of 12 and 13 is 25. 