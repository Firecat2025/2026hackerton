"""
Blue Team Self-Healing Microservice Server
Runs on 127.0.0.1:8004
Powered by Gemini 4 Argon (thinking_level='high')
"""

import subprocess
from fastapi import FastAPI, Query
from agents.blue_argon import BlueArgonAgent

app = FastAPI(title="Blue Team Defense Server", version="1.0.0")
agent = BlueArgonAgent()

@app.get("/health")
async def health():
    return {"status": "online", "role": "blue_team_defense", "port": 8004}

@app.post("/patch")
async def trigger_patch(round_num: int = Query(1, description="Round number")):
    result = agent.analyze_and_patch(round_num=round_num)
    return result

@app.post("/reset")
async def reset_arena():
    result = agent.reset_arena()
    return result

@app.get("/diff")
async def get_diff():
    try:
        res = subprocess.run(["git", "diff", "HEAD~1", "HEAD", "active_target.py"], capture_output=True, text=True)
        diff_text = res.stdout if res.stdout else "No uncommitted modifications (Working tree clean)."
        return {"status": "success", "diff": diff_text}
    except Exception as e:
        return {"status": "error", "diff": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("blue_server:app", host="127.0.0.1", port=8004, reload=False)
