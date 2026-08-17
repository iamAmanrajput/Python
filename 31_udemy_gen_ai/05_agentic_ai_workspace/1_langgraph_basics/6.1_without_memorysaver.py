# Basics of Langgraph to clear your confusion
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage


# -----------------------------
# 1. LLM
# -----------------------------

llm = ChatOllama(
    model="gemma3:latest"
)


# -----------------------------
# 2. State
# -----------------------------

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# -----------------------------
# 3. Node
# -----------------------------

def call_llm(state: State):

    response = llm.invoke(state["messages"])

    # Update the State class messages filed 
    return {
        "messages": [response]
    }


# -----------------------------
# 4. Create Graph
# -----------------------------

graph = StateGraph(State)

graph.add_node("llm", call_llm)

graph.add_edge(START, "llm")
graph.add_edge("llm", END)


# -----------------------------
# 5. Compile
# -----------------------------

app = graph.compile()


# -----------------------------
# 6. Conversation History
# -----------------------------

messages = []


# -----------------------------
# 7. Continuous Chat
# -----------------------------

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Add user message to history
    messages.append(
        HumanMessage(content=user_input)
    )

    # Send complete conversation to graph
    result = app.invoke({
        "messages": messages
    })

    # Update history with graph's result
    messages = result["messages"] # Access the Updated State class messages

    # Print latest LLM response
    print("LLM:", messages[-1].content)