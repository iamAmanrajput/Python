# Few Shot Prompting : The Model is Provided with a few examples before asking it to generate a response .

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY");


client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Few Shot Prompting: Directly Giving the instructions to the model and Few Examples to the Model
SYSTEM_PROMPT = """
You should only and only answer coding related questions. Do not answer anything else.
Your name is Alexa. If the user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output in JSON format

Output Format:
{
  "code": "string" or null,
  "isCodingQuestion": boolean
}


Examples:
Q: Can you explain the a + b whole square?
A: {{"code" : null, "isCodingQuestion":false }}

Q: Hey, write a code in Python for adding two numbers.
A: { "code": "def add(a, b):\n    return a + b", "isCodingQuestion": false }

"""



response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, write a code to print n numbers in js."}
    ]
)

print(response.choices[0].message.content)
# output
#  ```json
# {
#   "code": "function printNumbers(n) {\n  for (let i = 1; i <= n; i++) {\n    console.log(i);\n  }\n}\n\n// Example usage:\n// printNumbers(5); // This will print numbers from 1 to 5",
#   "isCodingQuestion": true
# }
# ```