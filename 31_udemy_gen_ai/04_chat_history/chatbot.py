"""
Chat Message History Example using LangChain

Goal:
- Maintain conversation history for different users/sessions.
- Each session_id has its own separate chat history.
- The model should remember previous messages within the same session.
- A different session should NOT have access to another session's history.

Example:
chat1 -> User tells the model: "My name is Krish"
chat2 -> Asks "What is my name?" -> Model doesn't know
chat1 -> Asks "What is my name?" -> Model remembers "Krish"
"""

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
    BaseChatMessageHistory
)
from langchain_core.runnables.history import RunnableWithMessageHistory


# --------------------------------------------------
# 1. Load Environment Variables
# --------------------------------------------------

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# 2. Initialize Groq LLM
# --------------------------------------------------

model = ChatGroq(
    model="qwen/qwen3.6-27b",
    groq_api_key=groq_api_key,
    reasoning_effort="none"
)


# --------------------------------------------------
# 3. Create an In-Memory Store
# --------------------------------------------------

# This dictionary stores chat history for each session.
# Example:
# {
#     "chat1": InMemoryChatMessageHistory(...),
#     "chat2": InMemoryChatMessageHistory(...)
# }

store = {}


# --------------------------------------------------
# 4. Function to Get/Create Session History
# --------------------------------------------------

def get_session_history(session_id: str) -> BaseChatMessageHistory:

    # Create new history if the session doesn't exist
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    # Return history for the requested session
    return store[session_id]


# --------------------------------------------------
# 5. Wrap Model with Message History
# --------------------------------------------------

# RunnableWithMessageHistory automatically:
# 1. Loads previous messages
# 2. Sends them to the model
# 3. Stores new user and AI messages

with_message_history = RunnableWithMessageHistory(
    model,
    get_session_history
)


# --------------------------------------------------
# 6. First Conversation - chat1
# --------------------------------------------------

config_chat1 = {
    "configurable": {
        "session_id": "chat1"
    }
}

response1 = with_message_history.invoke(
    [
        HumanMessage(
            content="Hi, my name is Krish and I am a Chief AI Engineer."
        )
    ],
    config=config_chat1
)

print("Chat 1 Response:")
print(response1.content)

# Expected Output:
# Hello Krish! Nice to meet you.
# (Exact response may vary depending on the LLM)


# --------------------------------------------------
# 7. Different Conversation - chat2
# --------------------------------------------------

config_chat2 = {
    "configurable": {
        "session_id": "chat2"
    }
}

response2 = with_message_history.invoke(
    [
        HumanMessage(
            content="What is my name?"
        )
    ],
    config=config_chat2
)

print("\nChat 2 Response:")
print(response2.content)

# Expected Output:
# I don't know your name.
#
# Reason:
# chat2 has a separate history and Krish introduced
# himself only in chat1.


# --------------------------------------------------
# 8. Ask Again Using chat1
# --------------------------------------------------

response3 = with_message_history.invoke(
    [
        HumanMessage(
            content="What is my name?"
        )
    ],
    config=config_chat1
)

print("\nChat 1 Response:")
print(response3.content)

# Expected Output:
# Your name is Krish.


# --------------------------------------------------
# 9. View Stored Chat History (Optional)
# --------------------------------------------------

print("\nChat 1 History:")
print(store["chat1"].messages)

print("\nChat 2 History:")
print(store["chat2"].messages)

# Chat 1 History:
# [HumanMessage(content='Hi, my name is Krish and I am a Chief AI Engineer.', additional_kwargs={}, response_metadata={}), AIMessage(content="Hello Krish! It's a pleasure to meet you. As a Chief AI Engineer, you're certainly at the forefront of some fascinating and rapidly evolving technology.\n\nHow can I assist you today? Whether you're looking for technical discussions, code reviews, architectural advice, or just want to brainstorm ideas, I'm here to help.", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 67, 'prompt_tokens': 26, 'total_tokens': 93, 'completion_time': 0.127605435, 'completion_tokens_details': None, 'prompt_time': 0.001570258, 'prompt_tokens_details': None, 'queue_time': 0.048199608, 'total_time': 0.129175693}, 'model_name': 'qwen/qwen3.6-27b', 'system_fingerprint': 'fp_2f860a3fc2', 'service_tier': 'on_demand', 'reasoning_effort': 'none', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fa333-a40a-7e81-8997-a6b20a1beb45-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 26, 'output_tokens': 67, 'total_tokens': 93}), HumanMessage(content='What is my name?', additional_kwargs={}, response_metadata={}), AIMessage(content='Your name is Krish.', additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 6, 'prompt_tokens': 107, 'total_tokens': 113, 'completion_time': 0.011658882, 'completion_tokens_details': None, 'prompt_time': 0.007278808, 'prompt_tokens_details': None, 'queue_time': 0.052780627, 'total_time': 0.01893769}, 'model_name': 'qwen/qwen3.6-27b', 'system_fingerprint': 'fp_fff3b79855', 'service_tier': 'on_demand', 'reasoning_effort': 'none', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fa333-a741-79a3-b417-a76732e89d18-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 107, 'output_tokens': 6, 'total_tokens': 113})]


# Chat 2 History:
# [HumanMessage(content='What is my name?', additional_kwargs={}, response_metadata={}), AIMessage(content="I don't know your name. As an AI assistant, I don't have access to your personal identity or private information unless you choose to share it with me in our conversation.\n\nIf you'd like, you can tell me your name, and I'll be happy to address you by it!", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 61, 'prompt_tokens': 17, 'total_tokens': 78, 'completion_time': 0.116018923, 'completion_tokens_details': None, 'prompt_time': 0.000864775, 'prompt_tokens_details': None, 'queue_time': 0.051970394, 'total_time': 0.116883698}, 'model_name': 'qwen/qwen3.6-27b', 'system_fingerprint': 'fp_3a782ca0f8', 'service_tier': 'on_demand', 'reasoning_effort': 'none', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, id='lc_run--019fa333-a66f-7a00-a784-b9ad91d8d08e-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 17, 'output_tokens': 61, 'total_tokens': 78})]
