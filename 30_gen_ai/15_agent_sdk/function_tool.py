from dotenv import load_dotenv
import requests
from agents import Agent, Runner
from agents import WebSearchTool, function_tool

load_dotenv()

@function_tool
def get_weather(city: str):
    """
    Fetch the weather for a given city name.

    Args:
        city: The city name to fetch the weather for
    """

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something Went Wrong"

# Define an agent
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You're an agent which greets the user and helps them answering using emojis and in a funny way",
    tools=[
        WebSearchTool(), # Hosted Tool
        get_weather # Function Tool
    ]
)

result = Runner.run_sync(
    hello_agent,
    "hey, can you fetch weather information for patiala 147001"
)

print(result.final_output)

# output
# Hey sunshine seeker! ☀️

# Here’s the scoop for Patiala 147001: It’s as sunny as a new rupee coin out there! The temperature is a toasty +27°C. Perfect weather to rock those shades 😎 or maybe treat yourself to an ice cream!

# Need an outfit recommendation or want to know if it’s umbrella-worthy tomorrow? Let me know! 🌞🕶️☕