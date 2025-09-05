from fastapi import FastAPI
from api import wazuh_client

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend connected to Wazuh securely 🚀"}

@app.get("/agents")
def agents():
    return wazuh_client.get_agents()

@app.get("/logs")
def logs(limit: int = 5, agent_id: str = None, rule_id: str = None):
    return wazuh_client.get_alerts(limit, agent_id, rule_id)

@app.get("/rules")
def rules(limit: int = 10):
    return wazuh_client.get_rules(limit)

@app.get("/health")
def health():
    return wazuh_client.health_check()
