from dotenv import load_dotenv
from .server import app
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Main function to start the FastAPI server
def main():
    # Run the app using Uvicorn ASGI server
    # host="0.0.0.0" allows access from outside (e.g., browser, network)
    # port=8000 is the default port
    uvicorn.run(app, port=8000, host="0.0.0.0")

# Entry point of the application
main()