# Streaming In Langgraph

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list,add_messages]

llm = ChatOllama(model="gemma3:latest")

memory = MemorySaver()

def superbot(state:State):
    return {"messages":llm.invoke(state["messages"])}

graph = StateGraph(State)

# Node
graph.add_node("SuperBot", superbot)

# Edges
graph.add_edge(START, "SuperBot")
graph.add_edge("SuperBot", END)

graph_builder = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
config2 = {"configurable": {"thread_id": "2"}}
config3 = {"configurable": {"thread_id": "3"}}

# result contains the updated graph state after execution

# result = graph_builder.invoke({
#     "messages": "Hi, My name is Aman And I like cricket"
# }, config=config)

# print(result)
# print(result["messages"][-1].content)

# stream_mode="updates" means:
# Har node ke execute hone ke baad state mein jo update/change hua hai,
# sirf wahi stream hoga, complete state nahi.

# for chunk in graph_builder.stream({
#     "messages": "Hi, My name is Aman And I like cricket"
# }, config=config2, stream_mode="updates"):
#     print(chunk)

# {'SuperBot': {'messages': AIMessage(content="Hi Aman! That's great to hear you like cricket! It's a fantastic sport. \n\nWhat do you enjoy most about it? Do you have a favorite team or player? \n\nLet me know if you want to talk about anything cricket-related – scores, strategies, famous matches, or anything else! 😄", additional_kwargs={}, response_metadata={'model': 'gemma3:latest', 'created_at': '2026-08-18T01:41:49.099239Z', 'done': True, 'done_reason': 'stop', 'total_duration': 12908204500, 'load_duration': 1321371100, 'prompt_eval_count': 20, 'prompt_eval_duration': 335023000, 'eval_count': 68, 'eval_duration': 11229034000, 'logprobs': None, 'model_name': 'gemma3:latest', 'model_provider': 'ollama'}, id='lc_run--01a01287-f93a-7163-9862-9aa45a95b2cc-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 20, 'output_tokens': 68, 'total_tokens': 88})}}

# Stream the graph execution and get the complete state after each step
# The HumanMessage is not added twice.
# stream_mode="values" returns the complete state after each step.
# First, it shows the initial state containing only the HumanMessage.
# After the SuperBot node runs, it shows the updated state containing
# both the HumanMessage and the AIMessage.
for chunk in graph_builder.stream({
    "messages": "Hi, My name is Aman And I like cricket"
}, config=config3, stream_mode="values"):
    print(chunk)

# {'messages': [HumanMessage(content='Hi, My name is Aman And I like cricket', additional_kwargs={}, response_metadata={},id='8a3eb21e-8527-4580-9fb8-903c9a223add')]}

# {'messages': [HumanMessage(content='Hi, My name is Aman And I like cricket', additional_kwargs={}, response_metadata={},id='8a3eb21e-8527-4580-9fb8-903c9a223add'), AIMessage(content="Hi Aman! It's great to meet you. Cricket is a fantastic sport - it's a real passion for so many people. \n\nWhat do you enjoy most about cricket? Do you have a favorite team, player, or maybe a particular format (Test, ODI, T20)? \n\nI'd love to chat more about it if you'd like!", additional_kwargs={}, response_metadata={'model': 'gemma3:latest', 'created_at': '2026-08-18T01:45:55.128027Z', 'done': True, 'done_reason': 'stop', 'total_duration': 16206137600, 'load_duration': 1515332200, 'prompt_eval_count': 20, 'prompt_eval_duration': 1103951000, 'eval_count': 79, 'eval_duration': 13462246000, 'logprobs': None, 'model_name': 'gemma3:latest', 'model_provider': 'ollama'}, id='lc_run--01a0128b-ad63-7562-a28d-f146e1d5dfed-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 20, 'output_tokens': 79, 'total_tokens': 99})]}