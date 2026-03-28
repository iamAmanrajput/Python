# Implement Indexing Phase of RAG

# Load environment variables (like API keys)
from dotenv import load_dotenv

# Helps to handle file paths easily
from pathlib import Path  

# Used to read and extract text from PDF
from langchain_community.document_loaders import PyPDFLoader  

# Used to split large text into small chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

# OpenAI embedding model (converts text → vectors)
from langchain_openai import OpenAIEmbeddings

# Stores vectors in Qdrant database
from langchain_qdrant import QdrantVectorStore


# Load .env file (for API keys)
load_dotenv()


# Get the path of the PDF file
pdf_path = Path(__file__).parent / "nodejs.pdf"


# Create loader to read the PDF
loader = PyPDFLoader(file_path=pdf_path)


# Load PDF → gives list of pages as documents
docs = loader.load()


# Print first page content + metadata
print(docs[0])


# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # max size of each chunk
    chunk_overlap=400  # overlap between chunks for better context
)

chunks = text_splitter.split_documents(documents=docs)


# Convert text chunks into vector embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# Store embeddings into Qdrant vector database
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",   # Qdrant server URL
    collection_name="learning_rag" # Collection name
)


# Final message after indexing
print("Indexing of Document done...")