# Implement Retrieval Phase of RAG

# ================== LOAD ENVIRONMENT VARIABLES ==================
# Load variables (like API keys) from .env file into the environment
from dotenv import load_dotenv
load_dotenv()

# ================== IMPORT REQUIRED LIBRARIES ==================
# OpenAI client for LLM responses
from openai import OpenAI

# Embedding model to convert text into vector representations
from langchain_openai import OpenAIEmbeddings

# Vector database integration (Qdrant)
from langchain_qdrant import QdrantVectorStore

# Initialize OpenAI client
openai_client = OpenAI()


# ================== INITIALIZE EMBEDDING MODEL ==================
# This model converts text into high-dimensional vectors
# IMPORTANT: Must match the model used during indexing
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# ================== CONNECT TO QDRANT VECTOR DATABASE ==================
# Connect to an existing Qdrant collection where embeddings are stored
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",       # URL of running Qdrant server
    collection_name="learning_rag",    # Name of the collection
    embedding=embedding_model,         # Embedding function used for queries
)


# ================== GET USER QUERY ==================
# Take input query from user
user_query = input("Ask Something: ")


# ================== RETRIEVAL STEP (CORE OF RAG) ==================
# Convert user query → embedding (done internally)
# Perform similarity search in vector DB to find relevant chunks
# 'k' defines how many top similar results to return
search_results = vector_db.similarity_search(
    query=user_query,
    k=4
)


# ================== BUILD CONTEXT ==================
# Convert retrieved documents into structured context
# This context will be passed to the LLM
context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
    f"File Location: {result.metadata.get('source', 'Unknown')}"
    for result in search_results
])


# ================== SYSTEM PROMPT ==================
# Instruction for LLM to strictly use provided context
SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Answer the user's query ONLY using the provided context below.
If the answer is not available in the context, say:
"I could not find the answer in the provided document."

Also include the page number reference whenever possible.

Context:
{context}
"""


# ================== GENERATION STEP ==================
# Send context + user query to LLM to generate final answer
response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)


# ================== OUTPUT RESULT ==================
# Print the generated response
print(f"🤖 : {response.choices[0].message.content}")