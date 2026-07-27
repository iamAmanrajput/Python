import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(
    model="qwen/qwen3.6-27b",
    groq_api_key=groq_api_key,
    reasoning_effort="none"
)

# Create a reusable prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English to French. Return only the translation."),
    ("user", "{input}")
])

# Convert AIMessage into a string
parser = StrOutputParser()

# Create LCEL chain
chain = prompt | model | parser

# Invoke the chain
result = chain.invoke({
    "input": "Hello How are you?"
})

print(result) # Bonjour. Comment allez-vous ?