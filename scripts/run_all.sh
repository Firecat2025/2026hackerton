#!/usr/bin/env bash
# Runs Full Vibe Defender Autonomous Cyber Arena Stack:
# Target (8002), Red Server (8003), Blue Server (8004), HUD (8080), Cloudflare Tunnel
set -e

export PATH="$HOME/.local/bin:$PATH"

echo "=== [1/5] Stopping any previously running python/tunnel services ==="
pkill -f "uvicorn" || true
pkill -f "cloudflared" || true
sleep 1

echo "=== [2/5] Starting Active Target App (Port 8002 with live reload) ==="
nohup uvicorn active_target:app --host 127.0.0.1 --port 8002 --reload > target.log 2>&1 &
echo "Target started on 127.0.0.1:8002 (PID: $!)"

echo "=== [3/5] Starting Red Attack Server (Port 8003) ==="
nohup python3 red_server.py > red.log 2>&1 &
echo "Red Server started on 127.0.0.1:8003 (PID: $!)"

echo "=== [4/5] Starting Blue Defense Server (Port 8004) ==="
nohup python3 blue_server.py > blue.log 2>&1 &
echo "Blue Server started on 127.0.0.1:8004 (PID: $!)"

echo "=== [5/5] Starting HUD Controller Server (Port 8080) ==="
nohup python3 -m uvicorn server:app --host 127.0.0.1 --port 8080 > server.log 2>&1 &
echo "HUD Server started on 127.0.0.1:8080 (PID: $!)"

sleep 2

echo "=== [Ready] Launching Cloudflare Tunnel for Port 8080 ==="
cloudflared tunnel --url http://localhost:8080
