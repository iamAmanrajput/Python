
# CHARACTER TEXT SPLITTER
from langchain_text_splitters import CharacterTextSplitter

speech = ""

with open("speech.txt") as f:
    speech = f.read()

# CharacterTextSplitter create karo
# separator="\n\n" -> text ko paragraph (double newline) ke basis par split karega
# chunk_size=100 -> har chunk me maximum 100 characters honge
# chunk_overlap=20 -> consecutive chunks me 20 characters common rahenge
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=20
)

text = text_splitter.create_documents([speech])

print(text)