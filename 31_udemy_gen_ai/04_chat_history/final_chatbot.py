"""
Simple RAG Application using LangChain, Chroma and Ollama

Goal:
1. Create sample documents.
2. Convert documents into embeddings.
3. Store embeddings in Chroma Vector Store.
4. Create a Retriever to find relevant documents.
5. Create a Prompt Template.
6. Build a RAG chain using LCEL.
7. Ask a question and generate an answer using retrieved context.

Flow:
Question
   ↓
Retriever
   ↓
Relevant Documents
   ↓
Prompt + Context
   ↓
LLM
   ↓
Answer
"""


# --------------------------------------------------
# 1. Import Required Libraries
# --------------------------------------------------

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------------------------
# 2. Initialize Embedding Model
# --------------------------------------------------

# Converts text into numerical vectors (embeddings)
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# --------------------------------------------------
# 3. Initialize LLM
# --------------------------------------------------

# This model will generate the final answer
llm = ChatOllama(
    model="gemma3:latest"
)


# --------------------------------------------------
# 4. Create Documents
# --------------------------------------------------

# Each Document contains:
# page_content -> actual text
# metadata     -> extra information about the text

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),

    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),

    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),

    Document(
        page_content="Parrots are intelligent birds capable of learning and mimicking sounds.",
        metadata={"source": "bird-pets-doc"},
    ),

    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]


# --------------------------------------------------
# 5. Create Chroma Vector Store
# --------------------------------------------------

# Convert documents into embeddings and store them
# inside the Chroma Vector Store

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
)


# --------------------------------------------------
# 6. Create Retriever
# --------------------------------------------------

# Retriever finds the most relevant document
# from the Vector Store for a given query

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)


# --------------------------------------------------
# 7. Test Retriever (Optional)
# --------------------------------------------------

# Search multiple queries at the same time
# and return relevant documents for each query

results = retriever.batch(["cat", "dog"])

# Uncomment to see retrieved documents
# print(results)


# --------------------------------------------------
# 8. Create RAG Prompt
# --------------------------------------------------

# The LLM should answer only using the
# context provided by the Retriever

message = """
Answer this question using the provided context only.

Question:
{question}

Context:
{context}
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("human", message)
    ]
)


# --------------------------------------------------
# 9. Create RAG Chain using LCEL
# --------------------------------------------------

# For the same user input:
#
# context  -> Retriever searches relevant documents
# question -> RunnablePassthrough passes original question
#
# Then:
# Retrieved Context + Question
#              ↓
#            Prompt
#              ↓
#             LLM

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
)


# --------------------------------------------------
# 10. Ask a Question
# --------------------------------------------------

response = rag_chain.invoke(
    "Tell me about dogs"
)


# --------------------------------------------------
# 11. Print Final Answer
# --------------------------------------------------

print(response.content)


# Expected Output:
# Dogs are great companions, known for their
# loyalty and friendliness.
#
# Exact output may vary depending on the LLM.