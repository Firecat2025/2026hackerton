#!/usr/bin/env bash
# VM Initialization Script for vibe-defender-vm (Ubuntu 22.04 LTS)
set -e

echo "=== [1/3] Updating System & Installing Python/Git ==="
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv git curl

echo "=== [2/3] Installing Cloudflare Tunnel (cloudflared) ==="
if ! command -v cloudflared &> /dev/null; then
    curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i /tmp/cloudflared.deb
    rm -f /tmp/cloudflared.deb
fi

echo "=== [3/3] Installing Python Dependencies ==="
pip3 install -r requirements.txt

echo "=== Setup Completed Successfully! ==="
