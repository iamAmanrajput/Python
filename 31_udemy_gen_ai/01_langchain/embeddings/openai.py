# Convert text into embedding vectors

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create an OpenAI Embeddings object
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Text to convert into an embedding vector
text = "This is a tutorial on OPENAI embedding"

# Generate the embedding vector
query_result = embeddings.embed_query(text)

# Print the embedding vector
print(query_result)

#Print dimensions
print(len(query_result)) #3072