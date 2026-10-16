#!/usr/bin/env bash
# Runs Target App (8002), HUD Server (8080), and Cloudflare Tunnel
set -e

export PATH="$HOME/.local/bin:$PATH"

echo "=== Starting Vibe Defender Services on Localhost (127.0.0.1) ==="

# 1. Start Vulnerable Target (Port 8002 with live reload)
echo "[1/3] Starting Active Target on 127.0.0.1:8002..."
nohup uvicorn active_target:app --host 127.0.0.1 --port 8002 --reload > target.log 2>&1 &
TARGET_PID=$!
echo "Target started (PID: $TARGET_PID)"

# 2. Start HUD & Orchestrator (Port 8080)
echo "[2/3] Starting HUD Server on 127.0.0.1:8080..."
nohup python3 -m uvicorn server:app --host 127.0.0.1 --port 8080 > server.log 2>&1 &
HUD_PID=$!
echo "HUD started (PID: $HUD_PID)"

sleep 2

# 3. Start Cloudflare Tunnel
echo "[3/3] Launching Cloudflare Tunnel for Port 8080..."
cloudflared tunnel --url http://localhost:8080
