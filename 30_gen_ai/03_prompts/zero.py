# Zero-shot Prompting: The model is given a direct question or task without prior examples.

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY");


client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Zero Shot Prompting: Directly Giving the instructions to the model
SYSTEM_PROMPT = "You should only and only answer coding related questions. Do not answer anything else. Your name is Alexa. If the user asks something other than coding, just say sorry."


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, tell me a joke."}
    ]
)

print(response.choices[0].message.content)
# output
# sorry