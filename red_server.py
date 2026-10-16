"""
Red Team Adversary Microservice Server
Runs on 127.0.0.1:8003
Powered by Gemini 4 Argon (thinking_level='medium')
"""

from fastapi import FastAPI, Query
from agents.red_argon import RedArgonAgent

app = FastAPI(title="Red Team Attack Server", version="1.0.0")
agent = RedArgonAgent()

@app.get("/health")
async def health():
    return {"status": "online", "role": "red_team_adversary", "port": 8003}

@app.post("/attack")
async def trigger_attack(
    scenario: str = Query("sqli_search", description="Attack type: sqli_search, auth_bypass, price_tampering"),
    level: int = Query(1, description="Difficulty level 1-3")
):
    result = agent.execute_attack(scenario=scenario, level=level)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("red_server:app", host="127.0.0.1", port=8003, reload=False)
