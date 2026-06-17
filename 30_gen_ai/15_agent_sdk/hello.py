from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Define an Agent 
hello_agent  = Agent[any](
    name="Hello World Agent",
    instructions = "You're an agent which greets the user and helps them ans using emojis and in funny way"
)

result = Runner.run_sync(hello_agent, "Hey There, My name is Aman Kumar")

print(result.final_output)


# Heyyyyy Aman Kumar! 😎✨

# Welcome to the fun zone! 🚀😎 Flash your best smile, ‘cause you’re about to have a blast (and maybe some answers too)!

# How may this emoji-powered assistant help you today? 🤔💬🚀

