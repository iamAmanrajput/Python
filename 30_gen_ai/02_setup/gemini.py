# Load environment variables from .env file
from dotenv import load_dotenv
import os
from google import genai

# .env file se variables load karta hai
load_dotenv()

# Environment variable se API key fetch kar rahe hain
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini client initialize kar rahe hain
client = genai.Client(
    api_key=api_key
)

# Model ko prompt bhej kar response generate kar rahe hain
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

# Model ka final text output print kar rahe hain
print(response.text)

# Expected Output:
# AI learns patterns from data to make smart decisions or predictions.
