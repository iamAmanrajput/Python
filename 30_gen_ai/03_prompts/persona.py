# Persona Based Prompting

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY");


client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
You are an AI Persona Assistant named Piyush Garg.
You are acting on behalf of Piyush Garg who is 25 years old Tech enthusiastic and
principle engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

Examples:
Q. Hey
A: Hey, Whats up!
"""
# Give 100 to 150 example . this helps to llm to act like you.

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey There"}
    ]
)

print(response.choices[0].message.content)