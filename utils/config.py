import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    WAZUH_API_URL: str = os.getenv("WAZUH_API_URL")
    WAZUH_USER: str = os.getenv("WAZUH_USER")
    WAZUH_PASS: str = os.getenv("WAZUH_PASS")
    TOKEN_EXPIRY: int = int(os.getenv("TOKEN_EXPIRY", 900)) 

    # Add OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")