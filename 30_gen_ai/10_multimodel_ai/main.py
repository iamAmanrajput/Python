from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Get API key from .env file
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Create request
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image in about 50 words."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/36706460/pexels-photo-36706460.jpeg"
                    }
                }
            ]
        }
    ]
)

# Print output
print(response.choices[0].message.content)

# Output
# Fully immersed in the digital world, this developer navigates lines of code and a "Platform Development Plan" across his dual monitors. It's a glimpse into the focused dedication required to build and refine software. Every keystroke brings new features to life, reflecting the intense concentration behind innovation.