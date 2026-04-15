# Implementation of LangGraph with LLM

from dotenv import load_dotenv

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

# init_chat_model is used to initialize a chat-based LLM (Large Language Model)
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
# This is used to securely access API keys (like OPENAI_API_KEY)
load_dotenv()

# Initialize the LLM (Large Language Model)
# model -> which model to use
# model_provider -> which company/provider (OpenAI here)
# This llm object will be used to generate responses
llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")


# Define the structure of the state that will flow through the graph
class State(TypedDict):
    # messages is a list that will store conversation history
    # Annotated is used to attach add_messages function
    # add_messages ensures new messages are appended (not replaced)
    messages: Annotated[list, add_messages]

# Define a node (function) in the graph
# This node takes the current state as input
# Chatbot node using LLM
def chatbot(state: State):
    """
    This node sends the current messages to the LLM
    and gets a response back.

    state.get("messages") -> retrieves conversation history
    llm.invoke(...) -> sends messages to LLM and gets response
    """

    response = llm.invoke(state.get("messages"))

    # Return response as a list (important for add_messages)
    return {
        "messages": [response]
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
# Updated State : {
#   'messages': [
#     HumanMessage(
#       content='Hi, My name is Aman Kumar',
#       additional_kwargs={},
#       response_metadata={},
#       id='b1a2c3d4-1111-2222-3333-abcdef123456'
#     ),

#     AIMessage(
#       content='Hello Aman Kumar! Nice to meet you. How can I assist you today?',
#       additional_kwargs={},
#       response_metadata={
#         'token_usage': {
#           'prompt_tokens': 15,
#           'completion_tokens': 20,
#           'total_tokens': 35
#         },
#         'model_name': 'gpt-4.1-mini'
#       },
#       id='c2b3d4e5-4444-5555-6666-fedcba654321'
#     ),

#     AIMessage(
#       content='Sample Message Appended',
#       additional_kwargs={},
#       response_metadata={},
#       id='d3c4e5f6-7777-8888-9999-xyz987654321'
#     )
#   ]
# }

# NOTE:
# Output messages are stored as LangChain message objects
# like HumanMessage / AIMessage (not plain strings)

# These objects contain:
# - content -> actual message text
# - metadata -> extra info (optional)
# - id -> unique identifier