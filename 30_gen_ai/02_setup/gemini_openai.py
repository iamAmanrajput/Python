from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY");


client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that." },
        { "role": "user", "content": "Hey, can you help me solve the a + b whole square"}
    ]
)

print(response.choices[0].message.content)

# output
# Yes, I can definitely help you with that!

# The expansion of $(a+b)^2$ is given by the algebraic identity:

# $(a+b)^2 = a^2 + 2ab + b^2$