import os
from dotenv import load_dotenv

# Get the directory of the current file (test_env.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file, assuming it's in the same directory
dotenv_path = os.path.join(current_dir, '.env')

print(f"Attempting to load .env from: {dotenv_path}")

# Load the environment variables
if load_dotenv(dotenv_path=dotenv_path):
    print(".env file loaded successfully!")
else:
    print("Failed to load .env file. Check file path and permissions.")

# Print the values of your API keys
print(f"HUNTER_API_KEY: {os.getenv('HUNTER_API_KEY')}")
print(f"APOLLO_API_KEY: {os.getenv('APOLLO_API_KEY')}")
print(f"NEWSAPI_API_KEY: {os.getenv('NEWSAPI_API_KEY')}")
print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")

# You can also add a check for the CRM keys if you like
print(f"CRM_API_KEY: {os.getenv('CRM_API_KEY')}")
print(f"CRM_API_BASE_URL: {os.getenv('CRM_API_BASE_URL')}")