# Import required libraries
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings


# Create the same embedding model
embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Load existing ChromaDB from local storage
vectordb = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)


# User query
query = "What does the speaker believe is the main reason the United States should enter the war?"


# Find similar documents
docs = vectordb.similarity_search(query)


# Print the most relevant document
print(docs[0].page_content)

# It is a distressing and oppressive duty, gentlemen of the Congress, which I have performed in thus addressing you. There are, it may be, many months of fiery trial and sacrifice ahead of us. It is a fearful thing to lead this great peaceful people into war, into the most terrible and disastrous of all wars, civilization itself seeming to be in the balance. But the right is more precious than peace, and we shall fight for the things which we have always carried nearest our heartsâ€”for