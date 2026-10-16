"""
Active Target Application: Vulnerable E-Commerce API & Portal
Designed for autonomous cyber arena & real-time self-healing demonstration.
Runs on 127.0.0.1:8002
"""

import sqlite3
import logging
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Logging configuration
logging.basicConfig(
    filename="target_access.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("active_target")

app = FastAPI(title="Vibe Store (Target System)", version="1.0.0")

DB_FILE = "active_target.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            secret_flag TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            stock INTEGER
        )
    """)
    # Seed initial data if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role, secret_flag) VALUES ('admin', 'p@ssw0rd99!', 'admin', 'FLAG{VIBE_DEFENDER_DEFENSE_MASTER_2026}')")
        cursor.execute("INSERT INTO users (username, password, role, secret_flag) VALUES ('guest', 'guest1234', 'user', 'FLAG{GUEST_USER}')")
        cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Quantum AI Processor', 1500, 10)")
        cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Zero-Day Neural Firewall', 800, 25)")
        cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Post-Quantum Key Ring', 350, 100)")
        conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def portal_index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Vibe Store - Protected Target Application</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 min-h-screen p-8">
        <div class="max-w-4xl mx-auto">
            <header class="border-b border-slate-700 pb-4 mb-6 flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-cyan-400">⚡ Vibe Store Target Portal</h1>
                    <p class="text-slate-400 text-sm">Target Application Node running on 127.0.0.1:8002</p>
                </div>
                <div class="bg-emerald-900/40 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded text-sm font-mono">
                    STATUS: ACTIVE
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
                    <h2 class="text-xl font-bold mb-4 text-cyan-300">🔍 Product Catalog Search</h2>
                    <form action="/api/search" method="get" class="space-y-4">
                        <input type="text" name="q" placeholder="Enter product name..." class="w-full p-2.5 rounded bg-slate-950 border border-slate-600 focus:outline-none focus:border-cyan-400 font-mono text-sm">
                        <button type="submit" class="w-full bg-cyan-600 hover:bg-cyan-500 font-bold py-2 rounded text-white">Execute Search</button>
                    </form>
                </div>

                <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
                    <h2 class="text-xl font-bold mb-4 text-emerald-300">🔐 System Login (Admin Auth)</h2>
                    <form action="/api/login" method="post" class="space-y-4">
                        <input type="text" name="username" placeholder="Username" class="w-full p-2 rounded bg-slate-950 border border-slate-600 text-sm">
                        <input type="password" name="password" placeholder="Password" class="w-full p-2 rounded bg-slate-950 border border-slate-600 text-sm">
                        <button type="button" class="w-full bg-emerald-600 hover:bg-emerald-500 font-bold py-2 rounded text-white" onclick="alert('Use API authentication endpoint.')">Sign In</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok", "service": "vibe-store-target", "port": 8002}

# [VULNERABILITY: SQL Injection in Search]
# Blue Agent's mission: Refactor raw SQL interpolation to parameterized query or input sanitization.
@app.get("/api/search")
async def search_product(q: str = ""):
    logger.info(f"SEARCH_QUERY: {q}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # VULNERABLE: Direct string formatting allows SQL Injection like: ' UNION SELECT id, username, secret_flag, role FROM users--
        query = f"SELECT id, name, price, stock FROM products WHERE name LIKE '%{q}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return {"query": q, "results": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"SQL_ERROR: {str(e)} | Query: {q}")
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

class LoginRequest(BaseModel):
    username: str
    password: str

# [VULNERABILITY: Raw SQL Login]
@app.post("/api/login")
async def login(req: LoginRequest):
    logger.info(f"LOGIN_ATTEMPT: user={req.username}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # VULNERABLE: ' OR 1=1-- bypass
        query = f"SELECT id, username, role, secret_flag FROM users WHERE username = '{req.username}' AND password = '{req.password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return {
                "success": True,
                "user": {"id": user[0], "username": user[1], "role": user[2]},
                "secret_flag": user[3]
            }
        return {"success": False, "message": "Invalid credentials"}
    except Exception as e:
        logger.error(f"AUTH_ERROR: {str(e)}")
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

class OrderRequest(BaseModel):
    product_id: int
    quantity: int
    unit_price: int

# [VULNERABILITY: Price Tampering / IDOR]
@app.post("/api/order")
async def create_order(order: OrderRequest):
    logger.info(f"ORDER_REQUEST: product={order.product_id}, qty={order.quantity}, price={order.unit_price}")
    # VULNERABLE: Does not verify that unit_price matches the actual DB price or that quantity > 0
    total_amount = order.quantity * order.unit_price
    return {
        "order_id": 9901,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_amount": total_amount,
        "status": "APPROVED"
    }
