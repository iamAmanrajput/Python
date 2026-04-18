# Load environment variables from .env file
from dotenv import load_dotenv

# OpenAI sync + async clients
from openai import OpenAI, AsyncOpenAI

# For making HTTP requests (used in weather API)
import requests

# Pydantic for structured output validation
from pydantic import BaseModel, Field

# Optional typing support
from typing import Optional

# JSON handling
import json

# OS commands execution
import os

# Async support
import asyncio

# Speech-to-text library
import speech_recognition as sr

# Audio player for TTS output
from openai.helpers import LocalAudioPlayer


# Load environment variables
load_dotenv()

# Initialize OpenAI clients
client = OpenAI()
async_client = AsyncOpenAI()


# -----------------------------
# TEXT TO SPEECH FUNCTION
# -----------------------------
async def tts(speech: str):
    """
    Converts text into speech and plays it.
    Uses streaming response for real-time audio playback.
    """
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",   # Lightweight TTS model
        voice="coral",             # Voice style
        instructions="Always speak in cheerfull manner with full of delight and happy",
        input=speech,
        response_format="pcm",     # Raw audio format
    ) as response:
        await LocalAudioPlayer().play(response)


# -----------------------------
# SYSTEM COMMAND TOOL
# -----------------------------
def run_command(cmd: str):
    """
    Executes a system command on user's machine.
    Dangerous: Should be used carefully.
    """
    result = os.system(cmd)
    return result


# -----------------------------
# WEATHER TOOL
# -----------------------------
def get_weather(city: str):
    """
    Fetch weather information using wttr.in API.
    Returns condition + temperature.
    """
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"


# -----------------------------
# AVAILABLE TOOLS MAP
# -----------------------------
available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}


# -----------------------------
# SYSTEM PROMPT (AGENT LOGIC)
# -----------------------------
SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    
    Workflow:
    START → PLAN → TOOL (optional) → OBSERVE → OUTPUT

    Rules:
    - Follow JSON format strictly
    - Only one step at a time
    - Think step-by-step before final answer

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }
"""


# -----------------------------
# OUTPUT STRUCTURE (Pydantic)
# -----------------------------
class MyOutputFormat(BaseModel):
    """
    Defines structured response format from LLM
    """
    step: str = Field(..., description="Step type: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="Message content")
    tool: Optional[str] = Field(None, description="Tool name")
    input: Optional[str] = Field(None, description="Tool input")


# -----------------------------
# MESSAGE HISTORY
# -----------------------------
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


# -----------------------------
# SPEECH RECOGNITION SETUP
# -----------------------------
r = sr.Recognizer()  # Create recognizer object

with sr.Microphone() as source:  # Access microphone
    r.adjust_for_ambient_noise(source)  # Remove background noise
    r.pause_threshold = 2  # Pause detection time

    while True:
        print("Speak Something...")
        
        # Capture audio from microphone
        audio = r.listen(source)

        print("Processing Audio... (STT)")
        
        # Convert speech → text using Google STT
        user_query = r.recognize_google(audio)

        # Add user input to chat history
        message_history.append({"role": "user", "content": user_query})

        # -----------------------------
        # AGENT LOOP (CHAINED EXECUTION)
        # -----------------------------
        while True:
            response = client.chat.completions.parse(
                model="gpt-4.1",
                response_format=MyOutputFormat,
                messages=message_history
            )

            # Raw string response
            raw_result = response.choices[0].message.content

            # Store assistant response
            message_history.append({"role": "assistant", "content": raw_result})

            # Parsed structured response
            parsed_result = response.choices[0].message.parsed


            # -----------------------------
            # START STEP
            # -----------------------------
            if parsed_result.step == "START":
                print("🔥", parsed_result.content)
                continue


            # -----------------------------
            # TOOL EXECUTION STEP
            # -----------------------------
            if parsed_result.step == "TOOL":
                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input

                print(f"🛠️: {tool_to_call} ({tool_input})")

                # Execute tool dynamically
                tool_response = available_tools[tool_to_call](tool_input)

                print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")

                # Add tool result as OBSERVE step
                message_history.append({
                    "role": "developer",
                    "content": json.dumps({
                        "step": "OBSERVE",
                        "tool": tool_to_call,
                        "input": tool_input,
                        "output": tool_response
                    })
                })
                continue


            # -----------------------------
            # PLAN STEP (Thinking)
            # -----------------------------
            if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                continue


            # -----------------------------
            # FINAL OUTPUT STEP
            # -----------------------------
            if parsed_result.step == "OUTPUT":
                print("🤖", parsed_result.content)

                # Convert response to speech
                asyncio.run(tts(speech=parsed_result.content))
                break

# Speak Something...
# Create Black Themed To-Do App
# Processing Audio... (STT)
# User wants to create a black themed to-do application. I'll first clarify what programming language or framework they'd like to use (e.g., React, Flutter, plain HTML/CSS/JS, etc.), as this will affect the guidance.

# Once the preferred technology is clarified, I will outline the UI design elements relevant for a black theme (background color, text color, button styling).

# Then, I’ll list the core features required for a basic to-do app: adding tasks, showing the task list, marking tasks as complete, and deleting tasks.

# Finally, I will provide or describe a sample code structure or template tailored to the chosen technology, incorporating the black theme styling and the core to-do app logic.

# To help you create a black themed to-do application, could you please specify which programming language or framework you want to use? (for example: React, Flutter, HTML/CSS/JavaScript, etc.) Once you let me know, I can provide a tailored step-by-step guide and code to get you started.

# Speak Something...
# Processing Audio... (STT)

# Given tool usage is an explicit request, I should demonstrate how run_command can generate needed files for the project (HTML, CSS, JS) and guide the user through the relevant steps. get_weather does not directly fit, but can be suggested as an extension (e.g., adding weather data for tasks) if needed.

# First, I’ll prepare the content for index.html, style.css, and script.js files with black theme styling and to-do app logic. Then, I’ll use run_command to create and populate these files on the user's system.

# I’ll start with creating an index.html file. This file will have the structure for the to-do app and link to 'style.css' and 'script.js'. I will use the run_command tool to create and populate this file on the user's system.

# After index.html is created, the next step is to generate the CSS file (style.css) that will apply a black theme to the app. I’ll use run_command to create and populate the CSS file with suitable styles.
