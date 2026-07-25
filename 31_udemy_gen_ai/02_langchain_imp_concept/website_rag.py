# ============================================================
# Simple GenAI RAG Application using LangChain
# ============================================================


# -------------------- IMPORTS --------------------

# Website se data/documents load karne ke liye
from langchain_community.document_loaders import WebBaseLoader

# Bade documents ko chhote chunks me split karne ke liye
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings ko store aur similarity search karne ke liye
from langchain_community.vectorstores import FAISS

# Documents ko context ke form me LLM ko dene ke liye
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# LLM ke liye prompt/template create karne ke liye
from langchain_core.prompts import ChatPromptTemplate

# Ollama ke local LLM ko LangChain ke saath use karne ke liye
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Manually Document object create karne ke liye
from langchain_core.documents import Document

# Retriever aur Document Chain ko combine karke RAG chain banane ke liye
from langchain_classic.chains import create_retrieval_chain


# ============================================================
# 1. LOAD DATA FROM WEBSITE
# ============================================================

# Website ka content load karta hai
loader = WebBaseLoader(
    "https://docs.smith.langchain.com/tutorials/Administrators/manage_spend"
)

# Website ke content ko Document objects me load karta hai
docs = loader.load()


# ============================================================
# 2. SPLIT DOCUMENTS INTO CHUNKS
# ============================================================

# Bade documents ko small chunks me divide karta hai
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # Har chunk me maximum approx 1000 characters
    chunk_overlap=200  # Chunks ke beech 200 characters common rahenge
)

# Loaded documents ko chunks me split karta hai
documents = text_splitter.split_documents(docs)


# ============================================================
# 3. CREATE EMBEDDINGS
# ============================================================

# Ollama embedding model text ko numerical vectors me convert karta hai
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ============================================================
# 4. CREATE FAISS VECTOR STORE
# ============================================================

# Document chunks ki embeddings create karke FAISS me store karta hai
# FAISS ki help se similar/relevant documents quickly search kar sakte hain
vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# ============================================================
# 5. INITIALIZE LLM
# ============================================================

# Gemma 3 local model ko LLM ke roop me use kar rahe hain
# Ye retrieved context ko samajh kar final answer generate karega
llm = ChatOllama(
    model="gemma3:latest"
)


# ============================================================
# 6. TEST SIMILARITY SEARCH FROM VECTOR STORE
# ============================================================

# Ye wo query hai jiske related documents hume search karne hain
query = "LangSmith has two usage limits: total traces and extended"

# FAISS query ke similar/relevant documents search karta hai
result = vectorstore.similarity_search(query)

# Sabse relevant document ka content print karta hai
print(result[0].page_content)

# cause, and resolve them with LangSmith Engine.For terminology and core concepts, refer to Observability concepts. For trace pricing, retention, and limits, see Usage and billing.To set up a LangSmith instance, visit the Platform setup section to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.


# ============================================================
# 7. CREATE PROMPT
# ============================================================

# LLM ko instruction dete hain ki answer sirf provided context
# ke basis par generate karna hai
prompt = ChatPromptTemplate.from_template(
    """
    Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question:
    {input}
    """
)


# ============================================================
# 8. CREATE DOCUMENT CHAIN
# ============================================================

# Document Chain context + question ko LLM ko deta hai
# aur LLM unke basis par answer generate karta hai
document_chain = create_stuff_documents_chain(
    llm,
    prompt
)


# ============================================================
# 9. TEST DOCUMENT CHAIN MANUALLY
# ============================================================

# Yaha hum manually context dekar Document Chain ko test kar rahe hain
document_response = document_chain.invoke({
    "input": "LangSmith has two usage limits: total traces and extended",

    "context": [
        Document(
            page_content=(
                "LangSmith has two usage limits: total traces and extended "
                "traces. These correspond to the two metrics we've been "
                "tracking on our usage graph."
            )
        )
    ]
})

print(document_response)

# LangSmith has two usage limits: total traces and extended traces.


# ============================================================
# 10. CREATE RETRIEVER
# ============================================================

# FAISS Vector Store ko Retriever me convert karta hai
# Retriever user ke question ke according relevant documents find karega
retriever = vectorstore.as_retriever()


# ============================================================
# 11. CREATE RETRIEVAL CHAIN
# ============================================================

# Retrieval Chain do kaam combine karti hai:
# 1. Retriever -> relevant documents find karta hai
# 2. Document Chain -> documents ko LLM ko dekar answer generate karti hai
retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)


# ============================================================
# 12. GET RESPONSE FROM LLM
# ============================================================

# User ka question Retrieval Chain ko dete hain
response = retrieval_chain.invoke({
    "input": "LangSmith has two usage limits: total traces and extended"
})


# ============================================================
# 13. DISPLAY FINAL ANSWER
# ============================================================

# LLM ka generated final answer
print(f"Answer: {response['answer']}")

# Answer: According to the context, "For trace pricing, retention, and limits, see Usage and billing." However, it doesn't explicitly state that LangSmith has *two* specific usage limits named "total traces" and "extended". It mentions tracing pricing, retention, and limits in general.


# ============================================================
# 14. DISPLAY RETRIEVED CONTEXT
# ============================================================

# Retriever ne Vector Store se jo relevant documents nikale hain
print(f"Context: {response['context']}")

# Context: [Document(id='cceefad6-67b6-4763-91d1-e7ea1998dbed', metadata={'source': 'https://docs.smith.langchain.com/tutorials/Administrators/manage_spend', 'title': 'LangSmith Observability - Docs by LangChain', 'description': 'Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.', 'language': 'en'}, page_content='cause, and resolve them with LangSmith Engine.For terminology and core concepts, refer to Observability concepts. For trace pricing, retention, and limits, see Usage and billing.To set up a LangSmith instance, visit the Platform setup section to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.'), Document(id='b4e3eb79-871d-474a-b13e-454ec0208ecc', metadata={'source': 'https://docs.smith.langchain.com/tutorials/Administrators/manage_spend', 'title': 'LangSmith Observability - Docs by LangChain', 'description': 'Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.', 'language': 'en'}, page_content="LangSmith Observability - Docs by LangChainDocumentation IndexFetch the complete documentation index at: /llms.txtUse this file to discover all available pages before exploring further.Skip to main contentInterrupt is coming to NYC and London this fall. Join the builders, engineers, and teams shaping what's next for agents. Get your tickets →Docs by LangChain home pageMonitorSearch...⌘KAsk AIGitHubTry LangSmithTry LangSmithSearch...NavigationLangSmith ObservabilityOverviewEngineTraceDebugObserveReferenceLangSmith ObservabilityLangSmith Observability provides full visibility into your LLM application: from individual traces to production-wide performance metrics.LangSmith works with many frameworks and providers. Browse available integrations to connect your stack including OpenAI, Anthropic, CrewAI, Vercel AI SDK, Pydantic AI, and more.Get startedCreate an accountSign up at smith.langchain.com (no credit card required)."), Document(id='34c14485-d1d3-4b28-ba54-10dddc2d37d9', metadata={'source': 'https://docs.smith.langchain.com/tutorials/Administrators/manage_spend', 'title': 'LangSmith Observability - Docs by LangChain', 'description': 'Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.', 'language': 'en'}, page_content='Copy the key and save it securely.Once your account and API key are ready, set up tracing:Set up tracingAdd tracing to your app in minutes with environment variables, framework integrations, or the SDK.Trace a RAG applicationFollow a step-by-step tutorial to instrument a retrieval-augmented generation app from start to finish.Investigate and monitorView tracesFilter, export, share, and compare traces via the UI or API.Monitor performanceBuild dashboards and set alerts to track quality and catch issues early.Configure automationsAutomate workflows with rules, webhooks, and online evaluations.Collect feedbackAnnotate outputs and gather user feedback using queues or inline annotation.Find and fix failures with EngineAutomatically detect recurring issues in your traces, diagnose their root cause, and resolve them with LangSmith Engine.For terminology and core concepts, refer to Observability concepts. For trace pricing, retention, and limits, see Usage and billing.To set up a LangSmith'), Document(id='6e5e2ec9-b2fe-435b-a38f-1153842640e7', metadata={'source': 'https://docs.smith.langchain.com/tutorials/Administrators/manage_spend', 'title': 'LangSmith Observability - Docs by LangChain', 'description': 'Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.', 'language': 'en'}, page_content='Connect these docs to Claude, VSCode, and more via MCP for real-time answers.Edit this page on GitHub or file an issue.⌘I')]