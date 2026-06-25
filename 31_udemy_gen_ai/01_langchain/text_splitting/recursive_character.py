# Recursive Character Text Splitter Example

# PDF load karne ke liye PyPDFLoader import kiya
from langchain_community.document_loaders import PyPDFLoader

# Large text ko meaningful chunks me split karne ke liye
from langchain_text_splitters import RecursiveCharacterTextSplitter

# PDF file load karo
loader = PyPDFLoader("attention.pdf")

# PDF ke saare pages ko Document objects ki list me convert karo
docs = loader.load()

# Text Splitter create karo
# chunk_size = har chunk me maximum 500 characters
# chunk_overlap = consecutive chunks me 50 characters common rahenge
# taaki context lose na ho
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Documents ko chhote-chhote chunks me split karo
final_document = text_splitter.split_documents(docs)

print(final_document)