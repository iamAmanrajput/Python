# Load environment variables from .env file
from dotenv import load_dotenv

# Import Memory class from mem0 library (used for long-term memory handling)
from mem0 import Memory

# Import os module to access environment variables
import os

# Import OpenAI client (used to interact with LLM)
from openai import OpenAI

# Import json module (used to format memory context into string)
import json

# Load all environment variables (like API keys)
load_dotenv()

# Initialize OpenAI client (API key will be picked automatically from environment)
client = OpenAI()

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration object for initializing memory system
config = {
    "version": "v1.1",  # Version of mem0 configuration

    # Embedder configuration (used to convert text into vector embeddings)
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"  # Embedding model for vector conversion
        }
    },

    # LLM configuration (used internally by mem0 for reasoning / memory extraction)
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1"  # Language model used by mem0
        }
    },

    # Vector database configuration (used to store long-term memory)
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",  # Qdrant running locally
            "port": 6333          # Default Qdrant port
        }
    }
}

# Initialize memory client using the above configuration
mem_client = Memory.from_config(config)

# Infinite loop for continuous user interaction
while True:
    # Take user input from terminal
    user_query = input("> ")

    # Search relevant memories from vector database based on current query
    # It returns only the most relevant past memories (not all)
    search_memory = mem_client.search(query=user_query, user_id="aman")

    # Extract memory results and format them into readable strings
    # Each memory contains an ID and the stored memory text
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results")
    ]

    # Create system prompt by injecting retrieved memories as context
    # This helps LLM understand user preferences/history before answering
    SYSTEM_PROMPT = f"""
    Here is the context about the user :
    {json.dumps(memories)}
    """

    # Send user input + memory context to LLM and get response
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # Injected memory context
            {"role": "user", "content": user_query}        # Current user query
        ]
    )

    # Extract AI response text from response object
    ai_response = response.choices[0].message.content

    # Print AI response
    print("Ai Response : ", ai_response)

    # Store conversation into long-term memory
    mem_client.add(
        user_id="aman",  # Unique identifier for the user
        messages=[
            {"role": "user", "content": user_query},       # User message
            {"role": "assistant", "content": ai_response}  # AI response
        ]
    )
    # mem0 automatically:
    # - Extracts important facts
    # - Identifies semantic / factual memory
    # - Converts data into embeddings
    # - Stores it in vector database (Qdrant)

    # Confirmation message after saving memory
    print("Memory has been saved...")



# Important Note:
# This behavior is handled automatically by mem0.
# - It behaves like factual, semantic, and episodic memory without manual handling

# mem0 stores user information in the database (Qdrant) and manages it intelligently.

# Example behavior:
# - If the user says: "My name is Aman"
#   → mem0 stores "Aman" as factual data in the database

# - If the user says: "I like ice cream at night"
#   → mem0 stores this as a preference in the database

# - If later the user says: "I don't like ice cream"
#   → mem0 automatically updates or removes the previous ice cream preference from the database

# This means:
# - Data is stored in the database (Qdrant)
# - mem0 automatically decides what to store, update, or delete


# > what is my name?
# Found Memories: ['ID: a56df7a3-aa4c-468f-88c3-f12990eda4a6\nMemory: Name is Aman Kumar']
# AI: Your name is Aman Kumar.
# Memory has been saved...

# > i like to eat pizza with corn and cheese
# Found Memories: ['ID: a56df7a3-aa4c-468f-88c3-f12990eda4a6\nMemory: Name is Aman Kumar']
# AI: That sounds delicious, Piyush! Pizza with corn and cheese is a great combo—sweetness from the corn pairs so nicely with the gooey cheese. Do you like to add any other toppings or sauces to your pizza?
# Memory has been saved...

# > can you suggest me what food can I order?
# Found Memories: ['ID: 0887c387-d678-45c9-afc2-0cbdbf97f54\nMemory: Likes to eat pizza with corn and cheese',
#                  'ID: a56df7a3-aa4c-468f-88c3-f12990eda4a6\nMemory: Name is Aman Kumar']

# AI: Since you like pizza with corn and cheese, how about ordering a delicious pizza with those toppings? 
# You could try a classic cheese pizza with corn added, or maybe a barbecue chicken pizza with corn and extra cheese for some variety. 
# If you want something different, you might also enjoy a cheesy corn quesadilla or a loaded nachos platter with corn and melted cheese. 
# Would you like me to suggest some restaurants or specific dishes?