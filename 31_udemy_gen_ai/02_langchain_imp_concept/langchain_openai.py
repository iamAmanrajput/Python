# Import required libraries
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Load environment variables from .env file
load_dotenv()


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Enable LangSmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# Create LLM
llm = ChatOpenAI(model="gpt-4o")


# Create chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert AI Engineer. Provide answers based on the questions."
        ),
        (
            "user",
            "{input}"
        )
    ]
)


# Create output parser to convert LLM response into string
output_parser = StrOutputParser()


# Create chain
chain = prompt | llm | output_parser


# Send input to the chain
response = chain.invoke(
    {
        "input": "Can you tell me about LangSmith?"
    }
)


# Print final response
print(response)


# LangSmith is a platform developed by LangChain for debugging, testing, monitoring, and evaluating LLM applications. It helps developers track LLM calls, inspect traces, analyze performance, and identify issues in their AI applications.