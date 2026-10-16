#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/PC/vibe-defender
pkill -f "blue_server.py" || true
pkill -f "server:app" || true
sleep 1
nohup python3 blue_server.py > blue.log 2>&1 &
nohup python3 -m uvicorn server:app --host 127.0.0.1 --port 8080 > server.log 2>&1 &
sleep 2
echo "HUD and Blue Server Reloaded!"
