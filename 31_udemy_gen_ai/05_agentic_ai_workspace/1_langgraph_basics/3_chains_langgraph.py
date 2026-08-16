# Chain Using LangGraph
# In this section, we will learn how to build a simple chain using LangGraph
# that uses 4 important concepts:

# 1. How to use chat messages as our graph state
# 2. How to use chat models in graph nodes
# 3. How to bind tools to our chat models
# 4. How to execute tool calls in our graph nodes

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage

messages = [AIMessage(content="Please tell me how can I help", name="LLMmodel")]

messages.append(
    HumanMessage(content="I want to learn coding", name="Aman")
)

messages.append(
    AIMessage(content="Which programming language you want to learn", name="LLMmodel")
)

messages.append(
    HumanMessage(content="I want to learn python programming language", name="Aman")
)

llm = ChatOllama(model="qwen3.5:0.8b")
# response = llm.invoke(messages)
# print(response)

# Define a tool that adds two numbers
def add(a: int, b: int) -> int:
    """
    Add a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int
    """
    return a + b


# Bind the tool with the LLM
llm_with_tools = llm.bind_tools([add])

# Send the user message to the LLM
response = llm_with_tools.invoke(
    [HumanMessage(content="What is 2 plus 2", name="Aman")]
)

# Print the LLM response and tool call
print(response)

# content='' additional_kwargs={} response_metadata={'model': 'qwen3.5:0.8b', 'created_at': '2026-08-16T02:53:36.651767Z','done': True, 'done_reason': 'stop', 'total_duration': 8647883800, 'load_duration': 1005136000, 'prompt_eval_count': 302, 'prompt_eval_duration': 2087501000, 'eval_count': 92, 'eval_duration': 5539595000, 'logprobs': None, 'model_name': 'qwen3.5:0.8b', 'model_provider': 'ollama'} id='lc_run--01a0087d-0c41-7b53-809a-da45a73459b9-0' tool_calls=[{'name': 'add', 'args': {'a': 2, 'b': 2}, 'id': '6d26c485-1b0b-4128-a81a-ad8beb5697e5', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 302, 'output_tokens': 92, 'total_tokens': 394}

13.10