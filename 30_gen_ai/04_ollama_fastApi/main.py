# FastAPI framework import kar rahe hain API banane ke liye
from fastapi import FastAPI, Body

# Ollama client import kar rahe hain taaki local LLM se connect ho sake
from ollama import Client

# FastAPI app ka object create kar rahe hain
app = FastAPI()

# Ollama client ko localhost pe connect kar rahe hain
# Default Ollama port: 11434
client = Client(
    host="http://localhost:11434"
)

# Root endpoint (GET request)
# Browser me http://localhost:8000/ open karne par ye chalega
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Chat endpoint (POST request)
# Ye endpoint user ka message lega aur LLM ko bhejega
@app.post("/chat")
def chat(
    message: str = Body(
        ...,  # Required field
        description="The message from the user"
    )
):
    """
    Ye function user ka message receive karta hai
    aur Ollama ke gemma:2b model ko bhejta hai.
    Fir model ka response return karta hai.
    """

    # LLM ko chat format me message bhej rahe hain
    response = client.chat(
        model="gemma:2b",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    # Model ka generated response return kar rahe hain
    return {
        "response": response.message.content
    }
