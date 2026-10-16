# 🛡️ Vibe Defender: Autonomous AI Cyber Arena & Live Code Evolution

> **Google DeepMind AI Hackathon 2026** (Track 4: Autonomous Agents & Developer Tools)  
> An autonomous cyber arena where an AI Red Team (Adversary) and Blue Team (Defender) battle in real time against a live production e-commerce target, dynamically refactoring source code, committing to Git, and hot-reloading with zero downtime.

[![Model: Gemini 4 Argon](https://img.shields.io/badge/Model-Gemini_4_Argon-blue?style=flat-square&logo=google)](https://ai.google.dev/)
[![Infrastructure: Google Cloud GCE](https://img.shields.io/badge/GCP-Compute_Engine-orange?style=flat-square&logo=googlecloud)](https://cloud.google.com/)
[![Tunnel: Cloudflare Zero Trust](https://img.shields.io/badge/Security-Zero_Inbound_Tunnel-yellow?style=flat-square&logo=cloudflare)](https://www.cloudflare.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=flat-square)](LICENSE)

---

## 📌 Key Highlights

1. **Live Autonomous Self-Healing**: When a vulnerability is exploited, the Blue Team AI Agent analyzes AST, rewrites the source code on the fly, commits to Git, and hot-reloads (`uvicorn --reload`) the production service with zero downtime.
2. **Dual-Argon Orchestration**:
   - **Red Argon Agent (`thinking_level="medium"`)**: Dynamically synthesizes polymorphic exploit payloads across SQL Injection, Authentication Bypass, and Business Logic Price Tampering.
   - **Blue Argon Agent (`thinking_level="high"`)**: Performs deep root-cause AST analysis, enforces database catalog validation, and generates secure parameterized patches.
3. **Closed Verification Loop (Auto-Battle)**: Red-Argon attacks (breach confirmed) ➔ Blue-Argon patches & commits ➔ Red-Argon re-attacks (exploit neutralized verified).
4. **Time-Machine Cyber HUD**: A cyberpunk operations dashboard featuring real-time packet telemetry, visual before/after code diffs, and an immutable Git commit time-travel browser.
5. **Zero-Inbound GCP Architecture**: Deployed on Google Cloud Engine (GCE) and published via Cloudflare Tunnel, strictly complying with enterprise cloud security requirements by leaving zero unsecured open inbound ports.

---

## 🏗️ Architecture

```
                       [ Cloudflare Zero-Trust Tunnel ]
                                     │ (Public HTTPS)
                                     ▼
                ┌─────────────────────────────────────────┐
                │       Cyber Arena HUD (Port 8080)       │
                │  - Real-Time Packet & Exploit Telemetry │
                │  - Visual Before/After Code Diff Viewer │
                │  - Git Commit Time-Machine Browser      │
                └────────────┬───────────────┬────────────┘
                             │               │
            ┌────────────────┴┐             ┌┴────────────────┐
            ▼                                 ▼
   [ Red Adversary Agent ]          [ Blue Defender Agent ]
    Port 8003 (Argon Medium)         Port 8004 (Argon High)
    - SQLi Search Exfiltration       - AST Source Code Patching
    - Admin Auth Bypass              - Automated Git Commits
    - Zero-Cost Price Tampering      - Fast Zero-Downtime Reload
            │                                 │
            │ (Exploit Attacks)               │ (Live Code Patches)
            ▼                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │     Active Target Application: Vibe Store (Port 8002)       │
  │  - E-Commerce Storefront: Hardware Catalog, Cart & Orders   │
  │  - Monitored by uvicorn hot-reload on active_target.py      │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Local & Cloud)

### 1. Prerequisites & Dependencies
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-gemini-api-key"
```

### 2. Deploy to Google Cloud GCE VM
```bash
# Transfer repository to GCE VM
gcloud compute scp --recurse . vibe-defender-vm:~/vibe-defender --zone=asia-northeast3-a

# Connect via SSH
gcloud compute ssh vibe-defender-vm --zone=asia-northeast3-a
```

### 3. Launch Full Cyber Arena Stack
```bash
cd ~/vibe-defender
./scripts/run_all.sh
```

---

## 🛡️ Hackathon Evaluation Scenario (1-Click Auto-Battle)

1. Open the **Cyber Arena HUD** at `http://127.0.0.1:8080` (or public Cloudflare Tunnel URL).
2. Click **`⚡ Start Auto-Battle`**:
   - **Round 1 (SQLi Search)**: Red Agent extracts confidential user flags. Blue Agent patches query parameterization. Re-attack fails (400 Protected).
   - **Round 2 (Auth Bypass)**: Red Agent bypasses admin login with tautology `' OR '1'='1'`. Blue Agent enforces bound credentials. Re-attack fails (401 Protected).
   - **Round 3 (Price Tampering)**: Red Agent tampers order unit price to $0. Blue Agent injects database catalog price verification. Re-attack fails (400 Tampering Detected).
3. Inspect the **Live Source Code Evolution** viewer to verify the exact before/after diffs committed to Git.
