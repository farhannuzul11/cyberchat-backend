import time
import requests
import urllib3
from utils.config import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = Config.WAZUH_API_URL
USERNAME = Config.WAZUH_USER
PASSWORD = Config.WAZUH_PASS
TOKEN_EXPIRY = Config.TOKEN_EXPIRY

# Cache JWT token
token_cache = {"token": None, "expiry": 0}

def get_token():
    """Get or refresh JWT token from Wazuh API."""
    global token_cache
    now = time.time()

    if token_cache["token"] and now < token_cache["expiry"]:
        return token_cache["token"]

    auth = requests.post(
        f"{BASE_URL}/security/user/authenticate",
        auth=(USERNAME, PASSWORD),
        verify=False,
    )
    auth.raise_for_status()
    token = auth.json()["data"]["token"]

    token_cache = {"token": token, "expiry": now + TOKEN_EXPIRY}
    return token

def call_wazuh(endpoint: str, params: dict = None):
    """Generic function to call Wazuh API with JWT."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{BASE_URL}{endpoint}"
    res = requests.get(url, headers=headers, params=params, verify=False)

    if res.status_code == 404:
        return {"error": f"Endpoint {endpoint} not found"}
    return res.json()

# Specific wrappers
def get_agents():
    return call_wazuh("/agents")

def get_alerts(limit=5, agent_id=None, rule_id=None):
    params = {"limit": limit, "pretty": "true"}
    if agent_id:
        params["agent_list"] = agent_id
    if rule_id:
        params["rule_ids"] = rule_id
    return call_wazuh("/alerts", params)

def get_rules(limit=10):
    return call_wazuh("/rules", {"limit": limit})

def health_check():
    return call_wazuh("/")
