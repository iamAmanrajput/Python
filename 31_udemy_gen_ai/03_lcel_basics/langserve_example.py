import os
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langserve import add_routes


# Load environment variables from the .env file
load_dotenv()

# Get the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize the Groq LLM
model = ChatGroq(
    model="qwen/qwen3.6-27b",
    groq_api_key=groq_api_key,
    reasoning_effort="none"
)


# Define the system prompt with a dynamic language variable
system_template = "Translate the following into {language}:"


# Create a reusable chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])


# Create an output parser to convert AIMessage into a string
parser = StrOutputParser()


# Create the LCEL chain
# Flow: Prompt Template -> LLM -> Output Parser
chain = prompt_template | model | parser


# Create the FastAPI application
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)


# Expose the LangChain chain as API routes using LangServe
add_routes(
    app,
    chain,
    path="/chain"
)


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )