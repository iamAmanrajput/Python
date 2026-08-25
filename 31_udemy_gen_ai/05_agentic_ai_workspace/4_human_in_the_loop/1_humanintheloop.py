from dotenv import load_dotenv
load_dotenv()

import os

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


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


# System Message
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)


## node definition

# Assistant node that sends the messages to the LLM
def assistant(state: MessagesState):
    return {
        "messages": [
            llm_with_tools.invoke([sys_msg] + state["messages"])
        ]
    }


# Graph
builder = StateGraph(MessagesState)


## Define nodes:

# Add the assistant node to the graph
builder.add_node("assistant", assistant)

# Add the tools node to execute the tool calls
builder.add_node("tools", ToolNode(tools))


## Define the Edges

# Start the graph with the assistant node
builder.add_edge(START, "assistant")

# Check whether the assistant wants to call a tool
builder.add_conditional_edges(
    "assistant",

    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is not a tool call -> tools_condition routes to END
    tools_condition,
)

# After executing the tool, send the result back to the assistant
builder.add_edge("tools", "assistant")


# Create memory to save the graph state
memory = MemorySaver()


# Human In the Loop

# Compile the graph and interrupt before the assistant node
graph = builder.compile(
    interrupt_before=["assistant"],
    checkpointer=memory
)


# Create a unique thread ID to maintain conversation state
thread = {"configurable": {"thread_id": "123"}}


# Provide the initial user input
initial_input = {
    "messages": HumanMessage(content="Multiply 2 and 3")
}


# Stream the graph events and print the latest message
for event in graph.stream(
    initial_input,
    thread,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()

# ================================ Human Message =================================

# Multiply 2 and 3

# Execution stops before the assistant node because
# we set interrupt_before=["assistant"].
# The current state is saved as a checkpoint.

# Continue the Execution to Assistant 
for event in graph.stream(
    None,
    thread,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()

# ================================ Human Message =================================

# Multiply 2 and 3
# ================================ Human Message =================================

# Multiply 2 and 3
# ================================== Ai Message ==================================
# Tool Calls:
#   multiply (3gz79c6q8)
#  Call ID: 3gz79c6q8
#   Args:
#     a: 2
#     b: 3
# ================================= Tool Message =================================
# Name: multiply

# 6

# Continue the execution of Assistant and then end
for event in graph.stream(
    None,
    thread,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()

# ================================ Human Message =================================

# Multiply 2 and 3
# ================================ Human Message =================================

# Multiply 2 and 3
# ================================== Ai Message ==================================
# Tool Calls:
#   multiply (deg1d7s0n)
#  Call ID: deg1d7s0n
#   Args:
#     a: 2
#     b: 3
# ================================= Tool Message =================================
# Name: multiply

# 6
# ================================= Tool Message =================================
# Name: multiply

# 6
# ================================== Ai Message ==================================

# The result of multiplying 2 and 3 is 6.