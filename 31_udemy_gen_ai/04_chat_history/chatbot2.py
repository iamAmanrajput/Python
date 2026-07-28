# Chat Message History Example using LangChain & Prompt Template & trim messages

"""
Chat Message History with Prompt Template and Message Trimming

Goal:
- Create a chatbot with conversation history.
- Store history separately for each session.
- Trim old messages before sending them to the LLM.
- Prevent conversation history from becoming too large.

Flow:
User Messages
    ↓
Message History
    ↓
Message Trimmer
    ↓
Prompt Template
    ↓
LLM
    ↓
Response
"""

import os
from operator import itemgetter
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    trim_messages,
)

from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
    BaseChatMessageHistory,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory


# --------------------------------------------------
# 1. Load Environment Variables
# --------------------------------------------------

# Load variables from the .env file
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# 2. Initialize Groq LLM
# --------------------------------------------------

model = ChatGroq(
    model="qwen/qwen3.6-27b",
    groq_api_key=groq_api_key,
    reasoning_effort="none",
)


# --------------------------------------------------
# 3. Create Prompt Template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Answer all questions to the best of your ability.",
        ),

        # Conversation messages will be inserted here
        MessagesPlaceholder(variable_name="messages"),
    ]
)


# --------------------------------------------------
# 4. Create Message Trimmer
# --------------------------------------------------

# Keep only recent messages within the token limit
trimmer = trim_messages(
    max_tokens=70,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partials=False,
    start_on="human",
)


# --------------------------------------------------
# 5. Create LCEL Chain
# --------------------------------------------------

# Get "messages" from input
#        ↓
# Trim messages
#        ↓
# Pass trimmed messages to prompt
#        ↓
# Send prompt to LLM

chain = (
    RunnablePassthrough.assign(
        messages=itemgetter("messages") | trimmer
    )
    | prompt
    | model
)


# --------------------------------------------------
# 6. Create In-Memory Chat Store
# --------------------------------------------------

# Each session_id will have its own chat history
store = {}


# --------------------------------------------------
# 7. Get or Create Session History
# --------------------------------------------------

def get_session_history(
    session_id: str,
) -> BaseChatMessageHistory:

    # Create a new history for a new session
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    # Return history of the requested session
    return store[session_id]


# --------------------------------------------------
# 8. Add Message History to the Chain
# --------------------------------------------------

# Wrap the complete trimming + prompt + model chain
# with conversation history support

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)


# --------------------------------------------------
# 9. Configure Session
# --------------------------------------------------

config = {
    "configurable": {
        "session_id": "chat1"
    }
}


# --------------------------------------------------
# 10. Sample Previous Conversation
# --------------------------------------------------

messages = [
    SystemMessage(content="You're a good assistant."),
    HumanMessage(content="Hi! I'm Bob."),
    AIMessage(content="Hi!"),
    HumanMessage(content="I like vanilla ice cream."),
    AIMessage(content="Nice!"),
    HumanMessage(content="What's 2 + 2?"),
    AIMessage(content="4"),
    HumanMessage(content="Thanks."),
    AIMessage(content="No problem!"),
    HumanMessage(content="Having fun?"),
    AIMessage(content="Yes!"),
]


# --------------------------------------------------
# 11. Ask a New Question
# --------------------------------------------------

response = with_message_history.invoke(
    {
        "messages": messages
        + [
            HumanMessage(
                content="What's my name?"
            )
        ]
    },
    config=config,
)


# --------------------------------------------------
# 12. Print Response
# --------------------------------------------------

print(response.content)

# Expected Output:
# Your name is Bob.
#
# Note:
# The exact response depends on which messages remain
# after trimming. If the message containing the user's
# name is removed due to the token limit, the model
# may not remember the name.