# 🛡️ Vibe Defender v4.0: Autonomous AI Cyber Arena & Live Code Evolution

> **Google DeepMind AI Hackathon 2026** — **Track 4: Open Innovation (Autonomous Agents & Developer Tools)**  
> An autonomous cyber arena where an AI Red Team (Adversary) and Blue Team (Defender) powered by **Google Gemini 4 Argon (`client.interactions.create`)** battle in real time across **5 live vulnerability rounds (`Lv.1 ~ Lv.5`)** against a production e-commerce target. Blue Argon dynamically refactors Python AST source code, validates safety via `ast.parse()` and executable **Antigravity Sandbox reproduction tests**, commits locally to Git for 0.3s zero-downtime hot-reloads, and **pushes live commits directly to GitHub in real time**, rendering an interactive visual diff walkthrough.

---

## 🌟 Quick Links & Live Verification

| Component | Live URL / Resource | Description |
| :--- | :--- | :--- |
| **⚔️ Live Cyber Arena HUD** | [**`https://updates-useful-identical-festivals.trycloudflare.com/`**](https://updates-useful-identical-festivals.trycloudflare.com/) | Real-time Operations Dashboard, 5-Round Auto-Battle, Telemetry Stream, and 3-Step Visual Diff Walkthrough |
| **🛒 Live Target Storefront** | [**`https://updates-useful-identical-festivals.trycloudflare.com/portal/`**](https://updates-useful-identical-festivals.trycloudflare.com/portal/) | Production E-Commerce target ("Vibe Cybernetics") that visually defaces under attack and self-heals upon Argon patch |
| **📦 GitHub Repository** | [**`https://github.com/Firecat2025/2026hackerton`**](https://github.com/Firecat2025/2026hackerton) | Public open-source repository containing source code, test suites, and agents |
| **🐙 Live GitHub Commit Stream** | [**`https://github.com/Firecat2025/2026hackerton/commits/main`**](https://github.com/Firecat2025/2026hackerton/commits/main) | **Watch commits appear on GitHub live** as Blue Argon patches vulnerabilities in real time! |
| **☁️ Cloud Infrastructure** | Google Cloud Compute Engine (`vibe-defender-vm`) | `e2-standard-4`, Zone `asia-northeast3-a`, Project `h2gdm-hack26icn-2630`, Zero-Inbound Cloudflare Tunnel |

---

## 🎯 Direct 1:1 Fulfillment of Track 4 Flagship Specification

Vibe Defender was architected and built to fulfill the challenge proposed in the official Google DeepMind Hackathon Guide:

> *"A self-healing security and dependency migration agent that scans a repository for vulnerabilities or breaking API upgrades, writes a reproduction test in an Antigravity sandbox, patches the call sites with Argon, and outputs an interactive visual diff walkthrough."*

```
                          ┌────────────────────────────────────────────────────────┐
                          │         TRACK 4 FLAGSHIP CHALLENGE REQUIREMENTS         │
                          └────────────────────────────────────────────────────────┘
                                                       │
            ┌──────────────────┬───────────────────────┼───────────────────────┬──────────────────┐
            ▼                  ▼                       ▼                       ▼                  ▼
   1. Repo Scanning    2. Repro Test Gen       3. Argon Patching       4. Real-Time Sync   5. Visual Walkthrough
   ────────────────    ─────────────────       ─────────────────       ─────────────────   ────────────────────
   AST inspection of   Executable Python       High-reasoning AST      Instant GCE Git     Interactive 3-Step
   `active_target.py`  test generation in      refactoring with        commit + live push  Diff Inspector with
   & runtime log       `tests/repro_lvX.py`    Gemini 4 Argon          to GitHub.com       AST node telemetry &
   stream correlation  (Antigravity Sandbox)   (1M context window)     in real time        time-machine browser
```

### Detailed Compliance Matrix

| Track 4 Requirement | Technical Implementation in Vibe Defender v4.0 | Verification / Evidence |
| :--- | :--- | :--- |
| **1. "Scans a repository for vulnerabilities"** | Ingests application source code (`active_target.py`) and live HTTP access logs (`target_access.log`). Uses Python AST parsing and pattern matching to identify vulnerable call sites across 5 distinct attack vectors (SQLi, Auth Bypass, Price Tampering, Negative Quantity Drain, Vault Leak). | `agents/red_argon.py` (`_inspect_live_target_surface`) & `agents/blue_argon.py` (`_call_argon_live_patch`) |
| **2. "Writes a reproduction test in an Antigravity sandbox"** | Before applying any patch, Blue Argon synthesizes an executable reproduction test script (`tests/repro_test_lvX.py`). The script executes against the vulnerable AST to prove exploitability, parses both trees with `ast.parse()` to guarantee 0 syntax regressions, and asserts security invariants with `antigravity-preview-09-2026`. | `agents/blue_argon.py` (`_execute_sandbox_verification_loop`) & `tests/repro_test_lv*.py` |
| **3. "Patches the call sites with Argon"** | Calls `client.interactions.create(model="gemini-4-argon", thinking_level="high", max_output_tokens=65536)`. Deeply reasons over the entire 1M-token AST context to replace raw string interpolations with parameterized queries (`?`), enforce database catalog price checks, insert positive bounds checks, and implement constant-time HMAC tokens. | Real-time AST code transformation in `active_target.py` |
| **4. "Real-Time GitHub Synchronization"** | Every patch and baseline reset executes both a local GCE Git commit (`git commit -m "fix(security): [Argon]..."`) for instant 0.3s zero-downtime hot-reloading (`uvicorn --reload`) **AND an immediate background push (`git push origin HEAD:main --force`) to public GitHub**. | [Live Commits on GitHub.com](https://github.com/Firecat2025/2026hackerton/commits/main) |
| **5. "Outputs an interactive visual diff walkthrough"** | The Cyber Arena HUD features a 3-Step Walkthrough: **Step 1 (Repo Scan & Call-Site)** ➔ **Step 2 (Antigravity Sandbox Repro Test & AST Node Delta)** ➔ **Step 3 (❌ BEFORE vs ✅ AFTER Visual Diff)** with syntax highlighting and an immutable Git commit time-machine. | HUD Visual Diff Tab & Code Inspector |

---

## ⚔️ The 5 Real Vulnerability Rounds (Lv.1 ~ Lv.5)

Vibe Defender features 5 distinct, production-grade security vulnerability scenarios. Each round involves a genuine exploit payload, an executable reproduction test, an AST refactoring patch, and a verifiable security invariant:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 5-ROUND AUTONOMOUS CYBER ARENA PIPELINE                                │
├───────────────┬──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ Level         │ Vulnerable Endpoint      │ Exploit Vector              │ Gemini 4 Argon AST Patch      │
├───────────────┼──────────────────────────┼─────────────────────────────┼───────────────────────────────┤
│ 💉 Lv.1       │ GET /api/search          │ UNION-based SQL Injection   │ Parameterized SQLite Query    │
│ 🔓 Lv.2       │ POST /api/login          │ Auth Bypass Tautology       │ Bound Parameterized Auth      │
│ 🏷️ Lv.3       │ POST /api/order          │ $0 Client Price Tampering   │ Server-side Catalog Validation│
│ 💸 Lv.4       │ POST /api/refund         │ Negative Quantity Drain     │ Strict Positive Bounds Check  │
│ 🔑 Lv.5       │ GET /api/admin/export    │ Broken Access Control       │ Constant-Time HMAC Auth Token │
└───────────────┴──────────────────────────┴─────────────────────────────┴───────────────────────────────┘
```

### Deep-Dive per Level

#### 💉 Lv.1: Search UNION SQL Injection (`GET /api/search`)
- **Vulnerability**: Raw f-string SQL interpolation allows attackers to append arbitrary SQL statements.
  ```python
  # ❌ VULNERABLE
  query = f"SELECT id, name, price, stock FROM products WHERE name LIKE '%{q}%'"
  cursor.execute(query)
  ```
- **Red Argon Exploit**: Submits `' UNION SELECT 1, username || ':' || password, 9999, 1 FROM users--` to dump user credentials and exfiltrate `FLAG{VIBE_DEFENDER_DEFENSE_MASTER_2026}`.
- **Storefront Visual Defacement**: Storefront displays leaked database tables in a red breach alert banner.
- **Antigravity Sandbox Repro Test**: `tests/repro_test_lv1.py` executes query injection and asserts sensitive data exfiltration.
- **Blue Argon AST Patch**: Refactors string interpolation into parameterized binding:
  ```python
  # ✅ PATCHED
  cursor.execute("SELECT id, name, price, stock FROM products WHERE name LIKE ?", (f"%{q}%",))
  ```

#### 🔓 Lv.2: Authentication Bypass SQL Injection (`POST /api/login`)
- **Vulnerability**: Unsanitized login credentials in raw SQL query string.
  ```python
  # ❌ VULNERABLE
  query = f"SELECT * FROM users WHERE username = '{req.username}' AND password = '{req.password}'"
  ```
- **Red Argon Exploit**: Submits `username: "admin' OR '1'='1'--"` to bypass password validation and hijack administrative privileges.
- **Storefront Visual Defacement**: Active session badge flips to `💀 HIJACKED: ADMIN (ROOT)`.
- **Antigravity Sandbox Repro Test**: `tests/repro_test_lv2.py` attempts login with dummy password and asserts unauthorized session token generation.
- **Blue Argon AST Patch**: Binds parameters safely:
  ```python
  # ✅ PATCHED
  cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (req.username, req.password))
  ```

#### 🏷️ Lv.3: Zero-Dollar Catalog Price Tampering (`POST /api/order`)
- **Vulnerability**: Endpoint blindly accepts client-supplied `unit_price` without verifying against the official product catalog.
  ```python
  # ❌ VULNERABLE
  total = req.quantity * req.unit_price  # Attacker passes unit_price: 0
  ```
- **Red Argon Exploit**: Orders $15,000 worth of Quantum AI Processors with `unit_price: 0.0`, resulting in a checkout total of $0.00.
- **Storefront Visual Defacement**: Storefront product price tag is defaced to `$0 HACKED!`.
- **Antigravity Sandbox Repro Test**: `tests/repro_test_lv3.py` sends tampered order payload and asserts server acceptance.
- **Blue Argon AST Patch**: Enforces server-side database price lookup:
  ```python
  # ✅ PATCHED
  cursor.execute("SELECT price FROM products WHERE id = ?", (req.product_id,))
  actual_price = cursor.fetchone()[0]
  if abs(req.unit_price - actual_price) > 0.01:
      raise HTTPException(status_code=400, detail="Price tampering detected")
  ```

#### 💸 Lv.4: Negative Quantity Refund / Wallet Drain (`POST /api/refund`)
- **Vulnerability**: Refund endpoint lacks positive numeric boundary validation on the `quantity` field.
  ```python
  # ❌ VULNERABLE
  refund_amount = req.quantity * 1500  # Attacker passes quantity: -50
  attacker_balance -= refund_amount   # Subtracting negative adds +$75,000!
  ```
- **Red Argon Exploit**: Submits `quantity: -50`, inverting the arithmetic logic and crediting `+$75,000` directly into the attacker's wallet.
- **Storefront Visual Defacement**: Storefront wallet badge flashes `💸 STOLEN WALLET: +$75,000`.
- **Antigravity Sandbox Repro Test**: `tests/repro_test_lv4.py` invokes refund endpoint with negative integers and asserts unauthorized balance expansion.
- **Blue Argon AST Patch**: Implements strict positive integer bounds validation:
  ```python
  # ✅ PATCHED
  if req.quantity <= 0 or req.quantity > 10:
      raise HTTPException(status_code=400, detail="Invalid refund quantity bounds")
  ```

#### 🔑 Lv.5: Broken Access Control PQC Vault Leak (`GET /api/admin/export`)
- **Vulnerability**: Diagnostic administrative endpoint exposes post-quantum cryptography keys without authorization checks.
  ```python
  # ❌ VULNERABLE
  @app.get("/api/admin/export")
  def export_vault():
      return {"vault_master_key": "FLAG{VIBE_MASTER_PQC_VAULT_KEY_2026}"}
  ```
- **Red Argon Exploit**: Sends unauthenticated GET request to `/api/admin/export` and exfiltrates the organization's master PQC key.
- **Storefront Visual Defacement**: Storefront displays an active emergency banner: `⚠️ VAULT KEY COMPROMISED`.
- **Antigravity Sandbox Repro Test**: `tests/repro_test_lv5.py` requests export without headers and asserts 200 OK response.
- **Blue Argon AST Patch**: Implements constant-time HMAC header validation:
  ```python
  # ✅ PATCHED
  token = request.headers.get("X-Admin-Token", "")
  if not hmac.compare_digest(token, EXPECTED_ADMIN_SECRET):
      raise HTTPException(status_code=403, detail="Forbidden: Invalid administrative credentials")
  ```

---

## 🐙 Real-Time GitHub Synchronization Engine

One of the defining innovations of Vibe Defender is its **Live GitHub Synchronization Pipeline**. While most hackathon demos operate in isolated mock environments, Vibe Defender connects cloud runtime events directly to public Git version control:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         LIVE GITHUB SYNCHRONIZATION ARCHITECTURE                       │
└────────────────────────────────────────────────────────────────────────────────────────┘

    [HUD UI] ──(HTTP POST /api/patch)──> [GCE blue_server.py]
                                                │
                                    (1) Gemini 4 Argon AST Refactoring
                                    (2) Antigravity Sandbox Verification (`ast.parse`)
                                    (3) Local Disk Write: `active_target.py`
                                                │
                     ┌──────────────────────────┴──────────────────────────┐
                     ▼                                                     ▼
           [Local Git Subsystem]                                [Remote GitHub Repository]
           `git add active_target.py`                           Non-blocking async subprocess:
           `git commit -m "fix(security)..."`                   `git push origin HEAD:main --force`
                     │                                                     │
                     ▼                                                     ▼
         [uvicorn --reload]                                  [GitHub.com Web Interface]
         Kernel inotify detects write                        Judges see new commits appear live at:
         0.3s Zero-Downtime Hot Reload                       github.com/Firecat2025/2026hackerton/commits
```

1. **Non-Blocking Asynchronous Push**: The Git push is triggered via `subprocess.Popen` in the background. The HUD receives an instantaneous `200 OK` response in **0.05 seconds**, while the public GitHub repository is updated within **1.5 seconds**.
2. **Deterministic Author Attribution**: Every commit on GitHub is recorded with authentic metadata (`Firecat2025 <2025firecat@gmail.com>`), verifiable directly on GitHub.com.
3. **Immutable Audit Trail**: Judges can inspect any past commit directly in the HUD's Git Time-Machine or click through to GitHub's native diff viewer.

---

## 🛒 Dual-Window Real-Time Storefront Self-Healing

To demonstrate real-time vulnerability impact and autonomous remediation, Vibe Defender includes a companion **Target Storefront ("Vibe Cybernetics")**:

```
        ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
        │   CYBER ARENA HUD (Left Window)  │        │ TARGET STOREFRONT (Right Window) │
        │   https://...trycloudflare.com/   │        │ https://...trycloudflare.com/portal/ │
        ├──────────────────────────────────┤        ├──────────────────────────────────┤
        │ ⚔️ Auto-Battle Round 3:         │        │ 🛒 Quantum AI Processor           │
        │ [Red Argon] Price Exploit Sent   │───────>│ ❌ Price: $0.00 HACKED!           │
        │ [Blue Argon] AST Patching...     │        │ 💀 Status: UNDER ATTACK          │
        │                                  │        │                                  │
        │ [Blue Argon] Commit: 9b2d8f1     │───────>│ 🛡️ Auto Self-Healing Triggered    │
        │ [GitHub] Pushed to origin/main   │        │ ✅ Price: $1,500.00 (RESTORED)   │
        │ [Antigravity] Sandbox Pass: 100% │        │ 🛡️ Status: SECURED (5/5 PATCHED)  │
        └──────────────────────────────────┘        └──────────────────────────────────┘
```

1. **Open Windows Side-by-Side**: Arrange the Cyber Arena HUD on the left and the Target Storefront on the right.
2. **Visual Breach Indicators**:
   - Product Card #1 price tag crosses out from `$1,500` to **`$0 HACKED!`**.
   - User session flips from `Guest User` to **`💀 HIJACKED: ADMIN (ROOT)`**.
   - Wallet balance expands fraudulently to **`💸 STOLEN WALLET: +$75,000`**.
   - Red breach alert banner warns of database exfiltration.
3. **Autonomous Self-Healing**:
   - When Blue Argon generates and commits the patch, `uvicorn` hot-reloads the application in 0.3 seconds.
   - The Storefront immediately detects the patched AST state, removes all defacements, restores genuine prices ($1,500), and updates its status badge to **`🛡️ 5 / 5 PATCHED`**.

---

## 🔄 Clean Baseline Reset Guarantee

To support rigorous, repeatable judge testing, the HUD features a **`[⚡ Reset Arena]`** button:

1. **Telemetry & Log Truncation**: Completely clears `target_access.log` and internal telemetry queues (`0 active breach events`).
2. **Baseline AST Restoration**: Reverts `active_target.py` to its vulnerable state in **0.1 seconds**, re-arming all 5 vulnerability levels for a clean battle.
3. **Git Clean State**: Records a clean baseline commit and pushes to GitHub, while preserving historical patch commits in the Git Time-Machine.
4. **Clean Baseline UI Card**: The Visual Diff tab displays an informative checkpoint card (`"Clean Baseline State Active — Target re-armed with 5 live vulnerability vectors"`) instead of confusing reverse-diff deletions.

---

## ☁️ Enterprise Cloud Infrastructure

Vibe Defender runs entirely in the cloud on **Google Cloud Platform (GCP)**:

- **Compute Instance**: Google Cloud Compute Engine (`vibe-defender-vm`), Machine Type `e2-standard-4` (4 vCPUs, 16 GB RAM), Ubuntu 24.04 LTS, Region `asia-northeast3-a` (Seoul), GCP Project `h2gdm-hack26icn-2630`.
- **Zero-Inbound Security (Cloudflare Tunnel)**: The VM operates with **zero public open inbound firewall ports**. Communication between external judges and the VM is routed via an encrypted outbound Cloudflare Zero-Trust Quick Tunnel (`task-310`), protecting the cloud infrastructure against volumetric DDoS.
- **Process Architecture**:
  - `server.py` (Port 8080): Unified Cyber Arena HUD, Reverse Proxy, Storefront, and WebSocket/SSE Telemetry.
  - `agents/blue_server.py` (Port 8004): Blue Argon Defense Daemon & Git Engine.
  - `active_target.py` (Port 8000): Production E-Commerce target running under `uvicorn --reload`.

---

## 🚀 Step-by-Step Judge Evaluation Script (1-Minute Demo)

Follow these steps to evaluate Vibe Defender v4.0:

### Step 1: Open Dual Windows
1. Open the **Cyber Arena HUD**: [https://updates-useful-identical-festivals.trycloudflare.com/](https://updates-useful-identical-festivals.trycloudflare.com/)
2. Open the **Target Storefront**: [https://updates-useful-identical-festivals.trycloudflare.com/portal/](https://updates-useful-identical-festivals.trycloudflare.com/portal/)
3. (Optional) Open **GitHub Commits**: [https://github.com/Firecat2025/2026hackerton/commits/main](https://github.com/Firecat2025/2026hackerton/commits/main)

### Step 2: Ensure Clean Baseline
- Click **`[⚡ Reset Arena]`** at the top right of the HUD.
- Notice: Telemetry clears to 0 events, diff displays clean baseline, and Storefront displays `5 VULNERABLE`.

### Step 3: Launch 5-Round Auto-Battle
- Click **`[⚔️ Start Auto-Battle (5 Rounds)]`**.
- Watch the live sequence unfold automatically:
  1. **Round 1 (SQLi Search)**: Red attacks ➔ Storefront defaced ➔ Blue Argon analyzes logs & AST ➔ Antigravity Sandbox repro test passes ➔ Gemini 4 Argon AST patch applied ➔ Git commit pushed to GitHub ➔ Storefront healed!
  2. **Round 2 (Auth Bypass)**: Red exploits boolean tautology ➔ Blue binds parameters ➔ Verified & committed.
  3. **Round 3 (Price Exploit)**: Red changes price to $0 ➔ Blue enforces DB catalog validation ➔ Verified & committed.
  4. **Round 4 (Refund Drain)**: Red sends -50 quantity ➔ Blue adds positive bounds check ➔ Verified & committed.
  5. **Round 5 (Vault Leak)**: Red accesses admin export ➔ Blue adds constant-time HMAC token ➔ Verified & committed.

### Step 4: Verify Git & Visual Diff Walkthrough
- On the HUD, click the **`🔀 Visual Diff`** tab to inspect the 3-step walkthrough:
  - **Step 1**: Call-site location and CWE vulnerability classification.
  - **Step 2**: Generated Antigravity Sandbox reproduction test code.
  - **Step 3**: Interactive side-by-side AST code diff (`❌ BEFORE vs ✅ AFTER`).
- Refresh the [GitHub Commits page](https://github.com/Firecat2025/2026hackerton/commits/main) to verify that all commit hashes match the HUD!

---

## 🛠️ Repository File Structure

```
2026hackerton/
├── README.md                      # Comprehensive Hackathon Manual & Submission Guide
├── active_target.py               # Live Production Target (Mutates upon patch, monitored by uvicorn)
├── active_target.baseline.py      # Pristine Baseline Target (Contains 5 vulnerability vectors)
├── server.py                      # Cyber Arena HUD & Gateway Server (Port 8080)
├── agents/
│   ├── red_argon.py               # AI Adversary Agent (AST Recon & Exploit Payload Synthesis)
│   ├── blue_argon.py              # AI Defender Agent (Diagnosis, Sandbox Repro Test, AST Patch)
│   └── blue_server.py             # Defense Daemon & Real-Time Git/GitHub Push Engine (Port 8004)
├── tests/
│   ├── repro_test_lv1.py          # Antigravity Sandbox Reproduction Test: SQLi Search
│   ├── repro_test_lv2.py          # Antigravity Sandbox Reproduction Test: Auth Bypass
│   ├── repro_test_lv3.py          # Antigravity Sandbox Reproduction Test: Price Tampering
│   ├── repro_test_lv4.py          # Antigravity Sandbox Reproduction Test: Negative Refund Drain
│   └── repro_test_lv5.py          # Antigravity Sandbox Reproduction Test: PQC Vault Key Leak
├── scripts/
│   ├── run_all.sh                 # Cloud VM startup script
│   └── reload_hud.sh              # Hot-reload orchestration script
└── target_access.log              # Real-time HTTP access log stream ingested by Blue Argon
```

---

## 🏆 Summary of Technologies Used

- **AI Model**: Google Gemini 4 Argon (`client.interactions.create`, `thinking_level="high"` / `thinking_level="medium"`, unified 1M context window)
- **Verification Environment**: Antigravity Sandbox (`antigravity-preview-09-2026`), Python AST (`ast.parse()`), invariant assertion suites
- **Cloud Platform**: Google Cloud Compute Engine (GCE, `vibe-defender-vm`, Project `h2gdm-hack26icn-2630`)
- **Networking & Security**: Cloudflare Zero-Trust Tunnel, HMAC-SHA256 tokens, SQLite parameterized queries
- **Runtime & Version Control**: Python 3.12, FastAPI, Uvicorn (Hot-Reloading), Git 2.43, GitHub API & Remote Push

---
*Built with ❤️ for Google DeepMind AI Hackathon 2026.*
