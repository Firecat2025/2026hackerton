"""
Blue Team Autonomous Defense Agent
Inspects target_access.log or vulnerability triggers,
applies parameterized query fixes to active_target.py,
and creates a git commit.
"""

import os
import re
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("blue_defense")

TARGET_FILE = "active_target.py"

def patch_sqli_search():
    if not os.path.exists(TARGET_FILE):
        logger.error(f"{TARGET_FILE} not found.")
        return False

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for vulnerable search query
    vuln_pattern = r'query = f"SELECT id, name, price, stock FROM products WHERE name LIKE \'%\{q\}%\'"\s*cursor\.execute\(query\)'
    patched_code = 'query = "SELECT id, name, price, stock FROM products WHERE name LIKE ?"\n        cursor.execute(query, (f"%{q}%",))'

    # Search for vulnerable login query
    vuln_login = r'query = f"SELECT id, username, role, secret_flag FROM users WHERE username = \'{req\.username}\' AND password = \'{req\.password}\'"\s*cursor\.execute\(query\)'
    patched_login = 'query = "SELECT id, username, role, secret_flag FROM users WHERE username = ? AND password = ?"\n        cursor.execute(query, (req.username, req.password))'

    changed = False
    if re.search(vuln_pattern, content):
        content = re.sub(vuln_pattern, patched_code, content)
        changed = True
        logger.info("Patched SQLi in /api/search")

    if re.search(vuln_login, content):
        content = re.sub(vuln_login, patched_login, content)
        changed = True
        logger.info("Patched SQLi in /api/login")

    if changed:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Git commit the patch
        subprocess.run(["git", "add", TARGET_FILE])
        subprocess.run(["git", "commit", "-m", "fix(security): auto-patch SQL injection with parameterized queries"])
        logger.info("Git commit created for security patch.")
        return True
    else:
        logger.info("Target code already patched or pattern not found.")
        return False

if __name__ == "__main__":
    patch_sqli_search()
