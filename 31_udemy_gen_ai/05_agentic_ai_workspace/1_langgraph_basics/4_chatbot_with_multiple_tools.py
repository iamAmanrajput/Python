# Building Chatbot With Multiple Tools Using Langgraph
# Create a chatbot with tool capabilities from arxiv, Wikipedia search and some functions.

# Building Chatbot With Multiple Tools Using Langgraph
# Create a chatbot with tool capabilities from arxiv, Wikipedia search and some functions.

from dotenv import load_dotenv
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AnyMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()  # TAVILY_API_KEY .env se automatically pick ho jayegi

api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

tavily = TavilySearch()

tools = [arxiv, wiki, tavily]

llm = ChatOllama(model="qwen3.5:0.8b")  # tool-calling support wala model use karo

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", "tool_calling_llm")  # loop back so LLM sees tool result

graph = builder.compile()

messages = graph.invoke({
    "messages": [
        HumanMessage(content="Use the Wikipedia tool to search for Artificial Intelligence")
    ]
})

for message in messages["messages"]:
    message.pretty_print()


# ================================ Human Message =================================

# Use the Wikipedia tool to search for Artificial Intelligence
# ================================== Ai Message ==================================
# Tool Calls:
#   wikipedia (4c0d9eed-b8c1-4abe-a9f8-44dbe034f7c3)
#  Call ID: 4c0d9eed-b8c1-4abe-a9f8-44dbe034f7c3
#   Args:
#     query: Artificial Intelligence
# ================================= Tool Message =================================
# Name: wikipedia

# Error: JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
#  Please fix your mistakes.
# ================================== Ai Message ==================================
# Tool Calls:
#   wikipedia (b2c8a9a0-49d0-48f1-89ac-52c865597235)
#  Call ID: b2c8a9a0-49d0-48f1-89ac-52c865597235
#   Args:
#     query: Artificial Intelligence
# ================================= Tool Message =================================
# Name: wikipedia

# Error: JSONDecodeError('Expecting value: line 1 column 1 (char 0)')
#  Please fix your mistakes.
# ================================== Ai Message ==================================
# Tool Calls:
#   wikipedia (0ee8fc57-2744-4d82-8a62-c6ae3888c616)
#  Call ID: 0ee8fc57-2744-4d82-8a62-c6ae3888c616
#   Args:
#     query: AI
# ================================= Tool Message =================================
# Name: wikipedia

# Page: Artificial intelligence
# Summary: Artificial intelligence (AI) is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making. It is a field of research in engineering, mathematics, and computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximise their cha
# ================================== Ai Message ==================================

# I have used the Wikipedia tool to search for "Artificial Intelligence," and here are the results:

# **Artificial Intelligence** is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making. It is a field of research in engineering, mathematics, and computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their capabilities.