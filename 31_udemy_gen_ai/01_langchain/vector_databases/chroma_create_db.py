# Import required libraries
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load text file
loader = TextLoader("speech.txt")
documents = loader.load()


# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0
)

splits = text_splitter.split_documents(documents)


# Create embedding model
embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Create ChromaDB and save it locally
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory="./chroma_db"
)

print("ChromaDB saved successfully!")