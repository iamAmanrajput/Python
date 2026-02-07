# dotenv library ka use environment variables (.env file) load karne ke liye hota hai
from dotenv import load_dotenv

# OpenAI ka official client import kar rahe hain
from openai import OpenAI

# .env file ke andar jo OPENAI_API_KEY hai usko memory me load kar deta hai
load_dotenv()

# OpenAI client ka object create kar rahe hain
# Ye automatically OPENAI_API_KEY ko env se read karta hai
client = OpenAI()

# Chat Completion API call
response = client.chat.completions.create(
    # Kaunsa model use karna hai
    model="gpt-4o-mini",

    # Conversation ka input
    # role="user" ka matlab user ka message
    messages=[
        {
            "role": "user",
            "content": "Hey There"
        }
    ]
)

# Response me multiple choices ho sakti hain
# Hum pehli choice ka message content print kar rahe hain
print(response.choices[0].message.content)

# output
# How can I help you today?