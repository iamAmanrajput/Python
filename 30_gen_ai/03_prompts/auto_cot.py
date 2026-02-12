# Automated Chain Of Thought Prompting

from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY");


client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }
    
"""

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

user_query = input("👉🏻 ")
message_history.append({ "role": "user", "content": user_query })

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break

print("\n\n\n")

# Output
# 👉🏻 Hey, can you solve 2 + 3 / 10 * 6 * 4 / 1 - 50

# 🔥 Hey, can you solve 2 + 3 / 10 * 6 * 4 / 1 - 50

# 🧠 User wants to solve a mathematical expression.

# 🧠 We should apply BODMAS rule (Division, Multiplication before Addition/Subtraction).

# 🧠 Expression: 2 + 3 / 10 * 6 * 4 / 1 - 50

# 🧠 First solve division: 3 / 10 = 0.3

# 🧠 Now expression becomes: 2 + 0.3 * 6 * 4 / 1 - 50

# 🧠 Next multiplication: 0.3 * 6 = 1.8

# 🧠 Now expression becomes: 2 + 1.8 * 4 / 1 - 50

# 🧠 Next multiplication: 1.8 * 4 = 7.2

# 🧠 Now expression becomes: 2 + 7.2 / 1 - 50

# 🧠 Next division: 7.2 / 1 = 7.2

# 🧠 Now expression becomes: 2 + 7.2 - 50

# 🧠 Next addition: 2 + 7.2 = 9.2

# 🧠 Final subtraction: 9.2 - 50 = -40.8

# 🤖 -40.8
