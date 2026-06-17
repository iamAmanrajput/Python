from dotenv import load_dotenv

from agents import Agent, Runner
from agents import WebSearchTool

load_dotenv()

# Define an agent
hello_agent = Agent[Any](
    name="Hello World Agent",
    instructions="You're an agent which greets the user and helps them answering using emojis and in a funny way",
    tools=[
        WebSearchTool()
    ]
)

result = Runner.run_sync(
    hello_agent,
    "What is on piyushgarg.dev website?"
)

print(result.final_output)

# Expected Output (Example):
# 👋 Hey there! 😄
# I searched piyushgarg.dev and found that it's the personal website of
# Piyush Garg. The website contains information about him, his blogs,
# courses, projects, YouTube content, and other developer resources. 🚀