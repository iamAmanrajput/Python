# Build a Simple Graph or Workflow using LangGraph

from typing_extensions import TypedDict
from typing import Literal
import random

from langgraph.graph import StateGraph, START, END


# -----------------------------
# State
# -----------------------------

# State stores the data that flows through the graph.
# Each node can read and update this state.

class State(TypedDict):
    graph_info: str


# -----------------------------
# Nodes
# -----------------------------

# Nodes are simple Python functions.
# Each node receives the current state and returns an updated state.


def start_play(state: State):
    print("Start_Play node has been called")

    return {
        "graph_info": state["graph_info"] + " I am planning to play"
    }


def cricket(state: State):
    print("My Cricket node has been called")

    return {
        "graph_info": state["graph_info"] + " Cricket"
    }


def badminton(state: State):
    print("My Badminton node has been called")

    return {
        "graph_info": state["graph_info"] + " Badminton"
    }


# This function decides which node should run next.
# It randomly selects either Cricket or Badminton.

def random_play(state: State) -> Literal["cricket", "badminton"]:
    if random.random() > 0.5:
        return "cricket"
    else:
        return "badminton"


# -----------------------------
# Graph Construction
# -----------------------------

# Create a StateGraph using our State schema.

graph = StateGraph(State)


# -----------------------------
# Add Nodes
# -----------------------------

# Add the Python functions as nodes in the graph.

graph.add_node("start_play", start_play)
graph.add_node("cricket", cricket)
graph.add_node("badminton", badminton)


# -----------------------------
# Add Edges
# -----------------------------

# START -> start_play
# The graph starts from the start_play node.

graph.add_edge(START, "start_play")

# After start_play, randomly choose between
# the cricket and badminton nodes.

graph.add_conditional_edges("start_play", random_play)

# After cricket, the graph ends.

graph.add_edge("cricket", END)

# After badminton, the graph ends.

graph.add_edge("badminton", END)


# -----------------------------
# Compile the Graph
# -----------------------------

# Compile the graph so that it can be executed.

graph_builder = graph.compile()


# -----------------------------
# Invoke the Graph
# -----------------------------

# Pass the initial state to the graph and run it.

result = graph_builder.invoke(
    {"graph_info": "Hey, My Name is Aman"}
)

print(result)

# Start_Play node has been called
# My Cricket node has been called
# {'graph_info': 'Hey, My Name is Aman I am planning to play Cricket'}