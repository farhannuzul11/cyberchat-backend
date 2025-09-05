from fastapi import FastAPI
import requests
import urllib3
import time
import os
from dotenv import load_dotenv

load_dotenv()
# Hides the SSL warning when calling Wazuh API over HTTPS with a self-signed cert.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = FastAPI()

BASE_URL = os.getenv("WAZUH_API_URL")
USERNAME = os.getenv("WAZUH_USER")
PASSWORD = os.getenv("WAZUH_PASS")

token_cache = {"token": None, "expiry": 0}

def get_token():
    """Get or refresh JWT token from Wazuh API."""
    global token_cache
    now = time.time()

    # Reuse if still valid
    if token_cache["token"] and now < token_cache["expiry"]:
        return token_cache["token"]

    # Otherwise, request new token
    auth = requests.post(
        f"{BASE_URL}/security/user/authenticate",
        auth=(USERNAME, PASSWORD),
        verify=False,
    )
    auth.raise_for_status()
    token = auth.json()["data"]["token"]

    # Cache for ~14 min
    token_cache = {"token": token, "expiry": now + 15 * 60}
    return token


@app.get("/")
def root():
    return {"message": "Backend connected to Wazuh securely 🚀"}


@app.get("/agents")
def get_agents():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/agents", headers=headers, verify=False)
    return res.json()

@app.get("/logs")
def get_alerts(limit: int = 5, agent_id: str = None, rule_id: str = None):
    """Fetch alerts with optional filters: limit, agent_id, rule_id."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit, "pretty": "true"}

    if agent_id:
        params["agent_list"] = agent_id
    if rule_id:
        params["rule_ids"] = rule_id

    res = requests.get(f"{BASE_URL}/alerts", headers=headers, params=params, verify=False)

    if res.status_code == 404:
        return {"error": "No alerts found. Try generating events (failed logins, file changes, etc.)"}
    return res.json()

@app.get("/rules")
def get_rules(limit: int = 10):
    """Fetch Wazuh rules (default: 10)."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit}
    res = requests.get(f"{BASE_URL}/rules", headers=headers, params=params, verify=False)
    return res.json()

@app.get("/health")
def health_check():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/", headers=headers, verify=False)
    return res.json()

