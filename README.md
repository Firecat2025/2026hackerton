# 🛡️ Vibe Defender v4.0: Autonomous AI Cyber Arena & Live Code Evolution

> **Google DeepMind AI Hackathon 2026** (Autonomous Agents & Developer Tools)  
> An autonomous cyber arena where an AI Red Team (Adversary) and Blue Team (Defender) powered by **Google Gemini 4 Argon (`client.interactions.create`)** battle across **5 live vulnerability rounds (`Lv.1 ~ Lv.5`)** against a production e-commerce target, dynamically refactoring Python AST source code, verifying via `ast.parse()` + Antigravity Sandbox (`antigravity-preview-09-2026`), committing to Git, and hot-reloading with zero downtime.

[![Model: Gemini 4 Argon](https://img.shields.io/badge/Model-Gemini_4_Argon-blue?style=flat-square&logo=google)](https://ai.google.dev/)
[![Verification: Antigravity Sandbox + AST](https://img.shields.io/badge/Verification-Antigravity_Sandbox_%2B_AST-purple?style=flat-square)](https://ai.google.dev/)
[![Infrastructure: Google Cloud GCE](https://img.shields.io/badge/GCP-Compute_Engine-orange?style=flat-square&logo=googlecloud)](https://cloud.google.com/)
[![Tunnel: Cloudflare Zero Trust](https://img.shields.io/badge/Security-Zero_Inbound_Tunnel-yellow?style=flat-square&logo=cloudflare)](https://www.cloudflare.com/)

---

## 📌 Key Highlights

1. **Authentic Dual-Argon Interactions API Architecture**:
   - **Red Argon Agent (`agents/red_argon.py`, `thinking_level="medium"`)**: Performs live target AST surface reconnaissance (`_inspect_live_target_surface`), autonomously picks the next unpatched vulnerability one-by-one (`Lv.1 ➔ Lv.5`), and synthesizes polymorphic exploit payloads via `client.interactions.create(model="gemini-4-argon")`.
   - **Blue Argon Agent (`agents/blue_argon.py`, `thinking_level="high"`)**: Ingests the full `active_target.py` source code + `target_access.log` breach telemetry into `gemini-4-argon` (`max_output_tokens=65536`), synthesizes exact `before_code ➔ after_code` patches, and executes a closed-loop verification before committing to Git.
2. **Closed-Loop AST & Antigravity Sandbox Verification (`_execute_sandbox_verification_loop`)**:
   - Every candidate patch is parsed into a Python Abstract Syntax Tree (`ast.parse()`) to verify **0 syntax regressions**, checked for security guard invariants, and verified against `antigravity-preview-09-2026` before disk write and `uvicorn --reload` hot-swap.
3. **5 Real Vulnerability Rounds (`Lv.1 ~ Lv.5`) & Real-Time Storefront Self-Healing**:
   - **Lv.1 (`GET /api/search`)**: Search UNION SQL Injection ➔ Parameterized SQLite query (`?`)
   - **Lv.2 (`POST /api/login`)**: Admin Auth Tautology Bypass (`' OR '1'='1'--`) ➔ Bound credential query
   - **Lv.3 (`POST /api/order`)**: Zero-Dollar Catalog Price Tampering (`$1,500 ➔ $0`) ➔ Server-side DB catalog price check
   - **Lv.4 (`POST /api/refund`)**: Negative Quantity Wallet Credit Drain (`quantity=-50 ➔ +$75,000`) ➔ Strict positive quantity & stock bounds check
   - **Lv.5 (`GET /api/admin/export`)**: Broken Access Control Master Key Leak ➔ Constant-time `hmac.compare_digest` Admin Token RBAC guard
4. **3-Tab Code Evolution Inspector & Interactive Git Time-Machine**:
   - Inspect **`🔀 Visual Diff`**, **`📜 Snapshot Code`**, and **`⚠️ Original Vulnerable`** code across every **`🛡️ ARGON PATCH`** and **`🔄 CLEAN RESET (Baseline)`** commit in the Git timeline.

---

## 🏗️ Architecture

```
                       [ Cloudflare Zero-Trust Tunnel ]
                                     │ (Public HTTPS)
                                     ▼
                ┌─────────────────────────────────────────┐
                │       Cyber Arena HUD (Port 8080)       │
                │  - 5-Round Auto-Battle & 1-by-1 Duel    │
                │  - 3-Tab Code Evolution Inspector       │
                │  - Interactive Git Commit Time-Machine  │
                └────────────┬───────────────┬────────────┘
                             │               │
            ┌────────────────┴┐             ┌┴────────────────┐
            ▼                                 ▼
   [ Red Adversary Agent ]          [ Blue Defender Agent ]
    Port 8003 (Argon Medium)         Port 8004 (Argon High)
    - Live Target AST Recon          - 1M Context AST Synthesis
    - Lv.1~Lv.5 Exploit Arsenal      - ast.parse() + Sandbox Loop
    - Polymorphic Payload Gen        - Automated Git Commits
            │                                 │
            │ (Exploit Attacks)               │ (Verified AST Patches)
            ▼                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │     Active Target Application: Vibe Store (Port 8002)       │
  │  - Real-Time Visual Breach Defacement & Automatic Healing   │
  │  - Monitored by uvicorn --reload on active_target.py        │
  └─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Local & Cloud)

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-gemini-api-key"
./scripts/run_all.sh
```
