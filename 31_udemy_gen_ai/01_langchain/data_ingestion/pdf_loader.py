# PDF LOADER

# Import PyPDFLoader to load a PDF file
from langchain_community.document_loaders import PyPDFLoader

# Create a PyPDFLoader object and specify the PDF file path
loader = PyPDFLoader("attention.pdf")

# Load the PDF and convert it into LangChain Document objects
pdf_documents = loader.load()

# Print the loaded Document objects
print(pdf_documents)

# Document object of First Page
print(pdf_documents[0])

# Print the content of each page
for page in pdf_documents:
    print(page.page_content)
    print("-" * 50)