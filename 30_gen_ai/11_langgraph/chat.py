# Implementation of LangGraph without LLM

# Import TypedDict for defining structured state
from typing_extensions import TypedDict

# Import Annotated to attach metadata (like add_messages)
from typing import Annotated

# add_messages is a helper that tells LangGraph how to update messages
from langgraph.graph.message import add_messages

# StateGraph is used to create the graph (workflow)
# START -> special node that represents the beginning of the graph execution
# END   -> special node that represents the termination (end) of the graph
from langgraph.graph import StateGraph, START, END


# Define the structure of the state that will flow through the graph
class State(TypedDict):
    # messages is a list that will store conversation history
    # Annotated is used to attach add_messages function
    # add_messages ensures new messages are appended (not replaced)
    messages: Annotated[list, add_messages]

# Define a node (function) in the graph
# This node takes the current state as input
def chatbot(state: State):
    return {
        "messages": ["Hi, This is a message from chatbot Node"]
    }

# ------------------ HOW STATE UPDATES WORK ------------------

# Initial state before node execution
# state = {
#     "messages": ["Hey There"]
# }

# Step 1: Node runs with current state
# chatbot(state = {"messages": ["Hey There"]})

# Step 2: Node returns new message
# return {"messages": ["Hi, This is a message from chatbot Node"]}

# Step 3: LangGraph automatically merges messages using add_messages
# (it APPENDS instead of replacing)

# Final updated state becomes:
# state = {
#     "messages": [
#         "Hey There",
#         "Hi, This is a message from chatbot Node"
#     ]
# }


def samplenode(state:State):
    return {
     "messages": ["Sample Message Appended"]
    }


# Initialize the graph builder with the defined State
# This tells LangGraph what kind of data will flow between nodes
graph_builder = StateGraph(State)


# Add a node to the graph
# Syntax:
# graph_builder.add_node("node_name", node_function)
# "chatbot"  -> This is the NODE NAME (a unique identifier in the graph)
# chatbot    -> This is the actual NODE FUNCTION (logic that will run)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode",samplenode)


# Define edges (flow of execution between nodes)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

# Flow representation:
# (START) → chatbot → samplenode → (END)


# Compile the graph into an executable object
# After this step, the graph is finalized and ready to run
graph = graph_builder.compile()

# Invoke (run) the compiled graph with an initial state
# Here we pass initial messages as input to start the flow
# The graph processes the input through defined nodes and edges
# updated_state will contain the final state after execution
updated_state = graph.invoke(State({"messages": ["Hi, My name is Aman Kumar"]}))
print("Updated State : ", updated_state)

# Output
# Updated State :  {'messages': [HumanMessage(content='Hi, My name is Aman Kumar', additional_kwargs={}, response_metadata={}, id='4b1ab113-b4ee-4a90-b9de-2a88cd7821c4'), HumanMessage(content='Hi, This is a message from chatbot Node', additional_kwargs={}, response_metadata={}, id='898b3eca-613c-438f-82f2-8c28a1238ce5'), HumanMessage(content='Sample Message Appended', additional_kwargs={}, response_metadata={}, id='e0ccb3a7-5971-4d1b-8485-ea3d84c06aec')]}