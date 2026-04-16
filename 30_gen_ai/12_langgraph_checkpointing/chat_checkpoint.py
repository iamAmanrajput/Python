# Implementation of LangGraph with LLM and Checkpointing

# Import environment variable loader
from dotenv import load_dotenv

# TypedDict for defining structured state
from typing_extensions import TypedDict

# Annotated helps attach metadata (like add_messages)
from typing import Annotated

# Utility to automatically append messages in state
from langgraph.graph.message import add_messages

# Core LangGraph components
from langgraph.graph import StateGraph, START, END

# Initialize LLM (Chat Model)
from langchain.chat_models import init_chat_model

# MongoDB-based checkpointing (for saving state)
from langgraph.checkpoint.mongodb import MongoDBSaver


# Load environment variables (API keys etc.)
load_dotenv()

# Initialize LLM model (OpenAI GPT-4.1 mini)
llm = init_chat_model(model="gpt-4.1-mini", model_provider="openai")


# Define State structure
# messages will be a list and automatically appended using add_messages
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Chatbot node function
def chatbot(state: State):
    # Send messages to LLM and get response
    response = llm.invoke(state.get("messages"))
    
    # Return updated state (append new response)
    return {
        "messages": [response]
    }


# Create graph builder with defined State
graph_builder = StateGraph(State)

# Add chatbot node
graph_builder.add_node("chatbot", chatbot)

# Define graph flow: START → chatbot → END
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile graph without checkpointing
graph = graph_builder.compile()


# Function to compile graph with checkpointing support
def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


# MongoDB connection URI
DB_URI = "mongodb://admin:admin@localhost:27017"

# Create MongoDB checkpointer (context manager ensures proper cleanup)
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    
    # Compile graph with checkpointing enabled
    graph_with_checkpointer = compile_graph_with_checkpointer(
        checkpointer=checkpointer
    )


# Configuration (thread_id helps maintain conversation memory)
config = {
    "configurable": {
        "thread_id": "aman"
    }
}


# Run graph in streaming mode
for chunk in graph_with_checkpointer.stream(
    State({"messages": ["Hi, My name is Aman Kumar"]}),
    config,
    stream_mode="values"
):
    # Print latest message in pretty format
    chunk["messages"][-1].pretty_print()


# Output
# ================================== AI Message ==================================

# Hello Aman Kumar! Nice to meet you 😊  
# How can I help you today?


# NOTE
# Main configuration me thread_id use karta hu jo ek unique identifier hota hai har user ya conversation ke liye.
# Jab tak same thread_id rehta hai, LangGraph us user ki puri conversation history (checkpoint) MongoDB me store karke yaad rakhta hai.
# Aur jaise hi thread_id change hota hai, system usko ek nayi conversation treat karta hai aur uska alag se memory track karna start kar deta hai.