# Chain Of Thought Prompting

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

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"},
   messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": "Hey, write a code to add n numbers in js."
    },

    # Manually keep adding messages to history
    {
        "role": "assistant",
        "content": json.dumps({
            "step": "START",
            "content": "You want a JavaScript code to add 'n' numbers."
        })
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "step": "PLAN",
            "content": "I need to provide a JavaScript function that can add any number of arguments or elements in an array. I will use the rest parameter syntax (...) to accept multiple numbers and then use the `reduce` method to sum them up."
        })
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "step": "PLAN",
            "content": "I need to provide a JavaScript function that can add any number of arguments or elements in an array. I will use the rest parameter syntax (...) to accept multiple numbers and then use the `reduce` method to sum them up."
        })
    },
    {
    "role": "assistant",
    "content": json.dumps({
        "step": "PLAN",
        "content": "I will define a JavaScript function that accepts an arbitrary number of arguments using the rest parameter. Inside the function, I will use the `reduce` array method to iterate over these arguments and calculate their sum. Finally, I will return the sum."
      })
    }

 ]

)

print(response.choices[0].message.content)