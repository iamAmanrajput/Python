# Runtime Input for Human-in-the-Loop
from dotenv import load_dotenv
load_dotenv()

import os

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage


# Get the Groq API key from the .env file
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Create the Groq LLM
llm_groq = ChatGroq(model="qwen/qwen3.6-27b")


### Custom tools

# Tool to multiply two numbers
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


# Tool to add two numbers
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


# Tool to divide two numbers
def divide(a: int, b: int) -> float:
    """Divide a by b.

    Args:
        a: first int
        b: second int
    """
    return a / b


# Store all custom tools in a list
tools = [add, multiply, divide]


# Bind the tools with the LLM so it can decide when to use them
llm_with_tools = llm_groq.bind_tools(tools=tools)


# system message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

## Human feedback node

def human_feedback(state: MessagesState):
    pass


### Assistant node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("human_feedback", human_feedback)

## Define the edges
builder.add_edge(START, "human_feedback")
builder.add_edge("human_feedback", "assistant")
# Check whether the assistant wants to call a tool
builder.add_conditional_edges(
    "assistant",

    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "human_feedback")

memory=MemorySaver()
graph=builder.compile(interrupt_before=["human_feedback"],checkpointer=memory)

# Input
initial_input = {
    "messages": [HumanMessage(content="Multiply 2 and 3")]
}

# Thread
thread = {"configurable": {"thread_id": "5"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

## get user input
# Update the graph state with the user's input.
# as_node tells LangGraph that this update is coming from the human_feedback node.
user_input=input("Tell me how you want to update the state:")
graph.update_state(
    thread,
    {"messages": [HumanMessage(content=user_input)]},
    as_node="human_feedback"
)

# Continue the graph execution
for event in graph.stream(None, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

# ================================ Human Message =================================

# Multiply 2 and 3
# Tell me how you want to update the state:please multiply 5 and 10
# ================================ Human Message =================================

# please multiply 5 and 10
# ================================== Ai Message ==================================
# Tool Calls:
#   multiply (sja151mgs)
#  Call ID: sja151mgs
#   Args:
#     a: 5
#     b: 10
# ================================= Tool Message =================================
# Name: multiply

# 50