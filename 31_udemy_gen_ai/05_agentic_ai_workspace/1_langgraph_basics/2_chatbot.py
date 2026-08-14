# Implementing a Simple Chatbot Using LangGraph

# Import required libraries
import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


# Load environment variables from the .env file
load_dotenv()


# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Define the State of the graph
# messages stores the conversation history
# add_messages tells LangGraph to add new messages instead of replacing them

class State(TypedDict):
    messages: Annotated[list, add_messages]


# Create the LLM models
llm = ChatOpenAI(model="gpt-4o")
llm_groq = ChatGroq(model="llama-3.3-70b-versatile")


# Create the chatbot node
# The node receives the current state and sends the messages to the LLM
def superbot(state: State):
    response = llm_groq.invoke(state["messages"])

    return {
        "messages": [response]
    }


# Create the LangGraph using our State
graph = StateGraph(State)


# Add the chatbot node to the graph
graph.add_node("Superbot", superbot)


# Connect START to the chatbot node
graph.add_edge(START, "Superbot")

# Connect the chatbot node to END
graph.add_edge("Superbot", END)


# Compile the graph so it can be executed
graph_builder = graph.compile()


# -----------------------------
# Invocation
# -----------------------------

# Run the chatbot with an initial message
result = graph_builder.invoke({
    "messages": "Hi, My name is Aman and I like cricket"
})

print(result)

# {'messages': [HumanMessage(content='Hi, My name is Aman and I like cricket', additional_kwargs={}, response_metadata={}, id='d30392dc-1a56-455a-b6d1-8b1c1f2ec46b'), AIMessage(content="Nice to meet you, Aman. Cricket is a fantastic sport, and I'm sure you must be excited about the various tournaments and leagues happening around the world. Which team or player is your favorite? Are you more into Test cricket, ODIs, or T20s?", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 57, 'prompt_tokens': 46, 'total_tokens': 103, 'completion_time': 0.177470013, 'completion_tokens_details': None, 'prompt_time': 0.001456689, 'prompt_tokens_details': None, 'queue_time': 0.16221175, 'total_time': 0.178926702}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_45180df409', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fff07-a735-7d21-ba6c-9528ad7cf95b-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 46, 'output_tokens': 57, 'total_tokens': 103})]}


# -----------------------------
# Streaming
# -----------------------------

# Stream the graph execution step by step
for chunk in graph_builder.stream({
    "messages": "Hello, My name is Krish"
}):
    print(chunk)

# {'Superbot': {'messages': [AIMessage(content="Hello Krish! It's nice to meet you. Is there something I can help you with or would you like to chat?", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 41, 'total_tokens': 67, 'completion_time': 0.046792308, 'completion_tokens_details': None, 'prompt_time': 0.004254538, 'prompt_tokens_details': None, 'queue_time': 0.050828812, 'total_time': 0.051046846}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_dae98b5ecb', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fff07-a934-7a43-a22f-3b8d3a7a1763-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 41, 'output_tokens': 26, 'total_tokens': 67})]}}

# Stream the graph and get the updated state after each step
for chunk in graph_builder.stream(
    {"messages": "Hello, My name is Krish"},
    stream_mode="values"
):
    print(chunk)

# {'messages': [HumanMessage(content='Hello, My name is Krish', additional_kwargs={}, response_metadata={}, id='8821938c-d64d-4417-a7c3-2aeacb0e2930')]}

# {'messages': [HumanMessage(content='Hello, My name is Krish', additional_kwargs={}, response_metadata={}, id='8821938c-d64d-4417-a7c3-2aeacb0e2930'), AIMessage(content="Hello Krish! It's nice to meet you. Is there something I can help you withor would you like to chat?", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 41, 'total_tokens': 67, 'completion_time': 0.051664468, 'completion_tokens_details': None, 'prompt_time': 0.001752127, 'prompt_tokens_details': None, 'queue_time': 0.050835713, 'total_time': 0.053416595}, 'model_name': 'llama-3.3-70b-versatile', 'system_fingerprint': 'fp_dae98b5ecb', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fff0b-c9c4-79a2-b327-5be739eec5f3-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 41, 'output_tokens': 26, 'total_tokens': 67})]}