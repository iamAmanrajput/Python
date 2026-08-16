# Example Of Langgraph with tools
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage
from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Reducer for handling message updates
from langgraph.graph.message import add_messages


# Initialize the LLM
llm = ChatOllama(model="qwen3.5:0.8b")


# Define a tool that adds two numbers
def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Sum of a and b
    """
    return a + b


# Bind the tool with the LLM
# This allows the LLM to decide when to call the add tool
llm_with_tools = llm.bind_tools([add])


# Define the state schema
class State(TypedDict):
    # add_messages reducer appends new messages
    # instead of replacing the existing messages
    messages: Annotated[list[AnyMessage], add_messages]


# Define the LLM node
def llm_tool(state: State):
    """
    Sends the current messages to the LLM.

    The LLM can either:
    1. Return a normal response
    2. Request a tool call
    """
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


# Create the graph builder
builder = StateGraph(State)


# Create a ToolNode containing our tools
tools = [add]
builder.add_node("tools", ToolNode(tools))

# Add the LLM node
builder.add_node("llm_tool", llm_tool)


# Start the graph with the LLM node
builder.add_edge(START, "llm_tool")


# Decide where to go after the LLM response:
#
# If the latest AI message contains a tool call
#     -> go to "tools"
#
# If there is no tool call
#     -> go to END
builder.add_conditional_edges(
    "llm_tool",
    tools_condition
)


# After the tool executes, send the tool result
# back to the LLM so it can generate the final response
builder.add_edge("tools", "llm_tool")

# END ki zarurat isliye nahi hai kyunki tools_condition already decide karta hai ki graph ko END par jaana hai ya tools node par.
# tools_condition already END ko routing option ke roop mein handle karta hai.


# Compile the graph
graph = builder.compile()


# Invoke the graph with the user's message
result = graph.invoke({
    "messages": [
       HumanMessage(content="What is 2 + 2? Use a tool call to calculate the answer.")
    ]
})


# Print the final state
print(result)


# {'messages': [HumanMessage(content='What is 2 + 2? Use a tool call to calculate the answer.', additional_kwargs={}, response_metadata={}, id='85214554-8f5a-4ef2-980e-223ed1822142'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'qwen3.5:0.8b', 'created_at': '2026-08-16T15:30:02.0262649Z', 'done': True, 'done_reason': 'stop', 'total_duration': 13177819400, 'load_duration': 1108379200, 'prompt_eval_count': 306, 'prompt_eval_duration': 2713369000, 'eval_count': 141, 'eval_duration': 9343378000, 'logprobs': None, 'model_name': 'qwen3.5:0.8b', 'model_provider': 'ollama'}, id='lc_run--01a00b31-812b-7be0-853e-7e6a1b186702-0', tool_calls=[{'name': 'add', 'args': {'a': 2, 'b': 2}, 'id': '4d6cec48-a834-4ab3-a793-65ecc67756c6', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 306, 'output_tokens': 141, 'total_tokens': 447}), ToolMessage(content='4', name='add', id='9b43085e-c353-4505-ac15-f2e94cb57ced', tool_call_id='4d6cec48-a834-4ab3-a793-65ecc67756c6'), AIMessage(content='2 + 2 = 4', additional_kwargs={}, response_metadata={'model': 'qwen3.5:0.8b', 'created_at': '2026-08-16T15:30:05.8413642Z', 'done': True, 'done_reason': 'stop', 'total_duration': 3807269500, 'load_duration': 983591500, 'prompt_eval_count': 359, 'prompt_eval_duration': 583408000, 'eval_count': 35, 'eval_duration': 2213835000, 'logprobs': None, 'model_name': 'qwen3.5:0.8b', 'model_provider': 'ollama'}, id='lc_run--01a00b31-b4b1-75a2-8660-c816f44bfc67-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 359, 'output_tokens': 35, 'total_tokens': 394})]}








# Flow 

# START
#   ↓
# llm_tool
#   ↓
# tools_condition
#   ↓
#   ├── Tool call hai → tools
#   │                    ↓
#   │                 llm_tool
#   │                    ↓
#   │              tools_condition
#   │                    ↓
#   │                  END
#   │
#   └── Tool call nahi hai → END