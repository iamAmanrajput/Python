from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import os

load_dotenv()

# Load Gemini API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI client with Gemini base URL
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


# Define state structure
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


# First LLM node
def chatbot(state: State):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": state.get("user_query")}]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


# Conditional decision function
def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    if True:
        return "endnode"
    return "chatbot_gemini"


# Second LLM node (fallback)
def chatbot_gemini(state: State):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": state.get("user_query")}]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


# Final node
def endnode(state: State):
    return state


# Create graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

# Define flow
graph_builder.add_edge(START, "chatbot")

# Conditional routing (FIXED: mapping added)
graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response,
    {
        "chatbot_gemini": "chatbot_gemini",
        "endnode": "endnode"
    }
)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

# Compile graph
graph = graph_builder.compile()

# Run graph with input
result = graph.invoke(State({"user_query": "Hey, What is 2 + 2 ?"}))

print(result)
# {'user_query': 'Hey, What is 2 + 2 ?', 'llm_output': '2 + 2 = 4'}