# Import the required modules
from dotenv import load_dotenv
import os

# Step 1: Load environment variables from .env file
load_dotenv()

# Step 2: Access the environment variables
mongoURl = os.getenv("MONGO_URL")
openAiKey = os.getenv("OPENAI_API_KEY")
