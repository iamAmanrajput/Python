# ============================
# Indexing Phase
# ============================

import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ----------------------------
# Load environment variables
# ----------------------------

# Load variables from the .env file
load_dotenv()

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# ----------------------------
# Create the embedding model
# ----------------------------

# Create an OpenAI embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# ----------------------------
# Load the text document
# ----------------------------

# Load the text file
loader = TextLoader("speech.txt")
docs = loader.load()


# ----------------------------
# Split the document into chunks
# ----------------------------

# Create a text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Split the document into smaller chunks
final_documents = text_splitter.split_documents(docs)


# ----------------------------
# Create the vector database
# ----------------------------

# Store document embeddings in Chroma
db = Chroma.from_documents(
    documents=final_documents,
    embedding=embeddings
)


# ----------------------------
# Generate an embedding
# ----------------------------

# Sample text
text = "This is a tutorial on OPENAI embedding"

# Convert the text into an embedding vector
query_result = embeddings.embed_query(text)

# Print the embedding vector
print(query_result)


# ----------------------------
# Similarity Search
# ----------------------------

# Search query
query = "It will be all the easier for us to conduct ourselves as belligerents"

# Find similar documents
retrieved_results = db.similarity_search(query)

# Print the retrieved documents
print(retrieved_results)