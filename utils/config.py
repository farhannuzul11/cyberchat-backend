import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    WAZUH_API_URL: str = os.getenv("WAZUH_API_URL", "https://127.0.0.1:55000")
    WAZUH_USER: str = os.getenv("WAZUH_USER", "wazuh")
    WAZUH_PASS: str = os.getenv("WAZUH_PASS", "wazuh")
    TOKEN_EXPIRY: int = int(os.getenv("TOKEN_EXPIRY", 15 * 60))