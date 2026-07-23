# Import required classes
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter


# Load the text file
loader = TextLoader("speech.txt")

# Initialize the Ollama embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Convert the text file content into LangChain Document objects
documents = loader.load()

# Initialize the text splitter
# chunk_size = maximum size of each chunk
# chunk_overlap = overlapping characters between consecutive chunks
text_splitter = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

# Split documents into smaller Document chunks
chunks = text_splitter.split_documents(documents)

# Generate embeddings for the chunks and store/index them in FAISS
db = FAISS.from_documents(chunks, embeddings)


# Query for similarity search
query = "What does the speaker believe is the main reason the United States should enter the war?"

# Find the most similar/relevant document chunks for the query
# docs = db.similarity_search(query)

# Print the content of the most relevant chunk
# print(docs[0].page_content)

# It is a distressing and oppressive duty, gentlemen of the Congress, which I have performed in thus addressing you. There are, it may be, many months of fiery trial and sacrifice ahead of us. It is a fearful thing to lead this great peaceful people into war, into the most terrible and disastrous of all wars, civilization itself seeming to be in the balance. But the right is more precious than peace, and we shall fight for the things which we have always carried nearest our heartsâ€”for democracy, for the right of those who submit to authority to have a voice in their own governments, for the rights and liberties of small nations, for a universal dominion of right by such a concert of free peoples as shall bring peace and safety to all nations and make the world itself at last free.

# Similarity search with score
docs_and_score = db.similarity_search_with_score(query)

print(docs_and_score)

# [(Document(id='2aa856a8-58f9-4f3d-86d5-e1978763996f', metadata={'source': 'speech.txt'}, page_content='It is a distressing and oppressive duty, gentlemen of the Congress, which I have performed in thus addressing you. There are, it may be, many months of fiery trial and sacrifice ahead of us. It is a fearful thing to lead this great peaceful people into war, intothe most terrible and disastrous of all wars, civilization itself seeming to be in the balance. But the right is more precious than peace, and we shall fight for the things which we have always carried nearest our heartsâ€”for democracy, for the right of those who submit to authority to have a voice in their own governments, for the rights and liberties of small nations, for a universal dominion of right by such a concert of free peoples as shall bring peace and safety to all nations and make the world itself at last free.'), np.float32(315.51978)), (Document(id='936914bd-1332-42c8-85b5-69e27a39c7ca', metadata={'source': 'speech.txt'}, page_content='It will be all the easier for us to conduct ourselves as belligerents in a high spirit of right and fairness because we act without animus, not in enmity toward a people or with the desire to bring any injury or disadvantage upon them, but only in armed opposition to an irresponsible government which has thrown aside all considerations of humanity and of right and is running amuck. We are, let me say again, the sincere friends of the German people, and shall desire nothing so much as the early reestablishment of intimate relations of mutual advantage between usâ€”however hard it may be for them, for the time being, to believe that this is spoken from our hearts.'), np.float32(323.2685)), (Document(id='1f256bfa-0c0e-4d96-b9ae-814c1097290b', metadata={'source': 'speech.txt'}, page_content='Just because we fight without rancor and without selfish object, seeking nothing for ourselves but what we shall wish to share with all free peoples, we shall, I feel confident, conduct our operations as belligerents without passion and ourselves observe with proud punctilio the principles of right and of fair play we profess to be fighting for.'), np.float32(333.8077)), (Document(id='7a0e544b-d500-410e-a36b-350c74cc2657', metadata={'source': 'speech.txt'}, page_content='To such a task we can dedicate our lives and our fortunes, everything that we are and everything that we have, with the pride of those who know that the day has come when America is privileged to spend her blood and her might for the principles that gave her birth and happiness and the peace which she has treasured. God helping her, she can do no other.'), np.float32(349.88815))]