"""
Active Target Application: Vulnerable E-Commerce API & Portal (v4.0 - 5 Vulnerability Levels)
Features 5 real, independent security vulnerabilities (Lv.1 ~ Lv.5), real-time visual breach state
on the Storefront, and automatic visual self-healing when Gemini 4 Argon patches each endpoint!
Runs on 127.0.0.1:8002
"""

import hmac
import logging
import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

logging.basicConfig(
    filename="target_access.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("active_target")

app = FastAPI(title="Vibe Store (Target System)", version="4.0.0")

DB_FILE = "active_target.db"

# Real-time visual state of the shopping mall so attacks from HUD or Store visibly alter the Storefront!
store_breach_state = {
    "sqli_leaked_data": None,
    "hijacked_admin": False,
    "hacked_price": None,
    "drained_wallet": None,
    "vault_exported": None,
}


def get_code_security_status():
    """Inspects own source code (active_target.py) to see which of the 5 vulnerabilities are patched by Argon."""
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            code = f.read()
        lv1_patched = ("WHERE name " + "LIKE ?") in code
        lv2_patched = ("WHERE username = ? " + "AND password = ?") in code
        lv3_patched = ("Price tampering " + "detected") in code
        lv4_patched = ("Negative refund quantity " + "blocked") in code
        lv5_patched = ("Unauthorized admin vault " + "access blocked") in code

        # Automatically heal visual breach state for any vulnerability that Argon has patched!
        if lv1_patched:
            store_breach_state["sqli_leaked_data"] = None
        if lv2_patched:
            store_breach_state["hijacked_admin"] = False
        if lv3_patched:
            store_breach_state["hacked_price"] = None
        if lv4_patched:
            store_breach_state["drained_wallet"] = None
        if lv5_patched:
            store_breach_state["vault_exported"] = None

        return {
            "lv1_search_sqli": "PATCHED" if lv1_patched else "VULNERABLE",
            "lv2_auth_bypass": "PATCHED" if lv2_patched else "VULNERABLE",
            "lv3_price_logic": "PATCHED" if lv3_patched else "VULNERABLE",
            "lv4_refund_drain": "PATCHED" if lv4_patched else "VULNERABLE",
            "lv5_vault_rbac": "PATCHED" if lv5_patched else "VULNERABLE",
            "patched_count": sum([lv1_patched, lv2_patched, lv3_patched, lv4_patched, lv5_patched]),
            "total_vulns": 5,
            "breach_state": store_breach_state,
        }
    except Exception:
        return {
            "lv1_search_sqli": "VULNERABLE",
            "lv2_auth_bypass": "VULNERABLE",
            "lv3_price_logic": "VULNERABLE",
            "lv4_refund_drain": "VULNERABLE",
            "lv5_vault_rbac": "VULNERABLE",
            "patched_count": 0,
            "total_vulns": 5,
            "breach_state": store_breach_state,
        }


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


@app.get("/api/security_status")
async def security_status():
    return get_code_security_status()


@app.get("/", response_class=HTMLResponse)
async def storefront():
    return """
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <title>Vibe Cybernetics Store — Quantum Hardware & Security</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
            body { font-family: 'Inter', sans-serif; background-color: #030712; color: #f8fafc; }
            .mono { font-family: 'JetBrains Mono', monospace; }
            .card-glow:hover { box-shadow: 0 0 30px rgba(56, 189, 248, 0.18); border-color: rgba(56, 189, 248, 0.5); }
            .breach-pulse { animation: pulseRed 1.5s infinite; }
            @keyframes pulseRed {
                0%, 100% { box-shadow: 0 0 25px rgba(244, 63, 94, 0.45); }
                50% { box-shadow: 0 0 45px rgba(244, 63, 94, 0.85); }
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col bg-slate-950 text-slate-100">
        <!-- Top Live Code Defense Shield Bar (5 Vulnerability Levels) -->
        <div class="bg-slate-900 border-b border-slate-800 px-6 py-2.5 text-xs mono flex flex-wrap justify-between items-center gap-3">
            <div class="flex items-center space-x-2">
                <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span class="font-bold text-slate-300">LIVE TARGET SOURCE STATUS (<span class="text-cyan-400">active_target.py</span>):</span>
            </div>
            <div class="flex flex-wrap items-center gap-2">
                <span id="badge-lv1" class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold">Lv.1 Search: VULNERABLE</span>
                <span id="badge-lv2" class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold">Lv.2 Auth: VULNERABLE</span>
                <span id="badge-lv3" class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold">Lv.3 Price: VULNERABLE</span>
                <span id="badge-lv4" class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold">Lv.4 Refund: VULNERABLE</span>
                <span id="badge-lv5" class="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold">Lv.5 Vault: VULNERABLE</span>
                <span id="shield-summary" class="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">0 / 5 PATCHED</span>
            </div>
        </div>

        <!-- Store Navigation Header -->
        <nav class="bg-slate-900/80 backdrop-blur-md border-b border-slate-800/80 px-8 py-4 sticky top-0 z-40">
            <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                        <i class="fa-solid fa-microchip text-white text-lg"></i>
                    </div>
                    <div>
                        <span class="text-xl font-extrabold tracking-tight text-white">VIBE <span class="text-cyan-400">CYBERNETICS</span> STORE</span>
                        <span class="block text-[11px] text-slate-400 mono">Enterprise AI & Quantum Hardware Marketplace • Port 8002</span>
                    </div>
                </div>

                <!-- Search Bar -->
                <div class="flex-1 max-w-md mx-4">
                    <div class="relative flex">
                        <input id="search-input" type="text" placeholder="Search hardware catalog (e.g. Quantum, Neural)..."
                            class="w-full bg-slate-950 border border-slate-700 rounded-l-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-cyan-400 mono">
                        <button onclick="searchCatalog()" class="bg-cyan-600 hover:bg-cyan-500 text-white px-5 py-2 rounded-r-xl text-sm font-bold transition">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </button>
                    </div>
                </div>

                <!-- Session Status Pill + Admin Login Form -->
                <div class="flex items-center space-x-3">
                    <div id="session-pill" class="px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-xs font-bold text-slate-300 mono flex items-center space-x-1.5">
                        <i class="fa-solid fa-user-astronaut text-cyan-400"></i>
                        <span id="session-text">Session: Guest ($0 Credit)</span>
                    </div>
                    <input id="login-user" type="text" placeholder="Username" class="w-24 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs mono text-white">
                    <input id="login-pass" type="password" placeholder="Password" class="w-24 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs mono text-white">
                    <button onclick="submitLogin()" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-3.5 py-2 rounded-lg transition">
                        <i class="fa-solid fa-lock-open mr-1"></i>Login
                    </button>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="max-w-7xl mx-auto w-full px-8 py-6 flex-1 space-y-6">
            <!-- REAL-TIME VISUAL BREACH DEFACEMENT BANNER -->
            <div id="live-breach-banner" class="hidden breach-pulse bg-rose-950/90 border-2 border-rose-500 rounded-2xl p-5 text-rose-100">
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-3">
                        <i class="fa-solid fa-skull-crossbones text-2xl text-rose-400"></i>
                        <div>
                            <h2 class="text-lg font-extrabold text-rose-300 uppercase tracking-wider">🚨 SYSTEM COMPROMISED BY RED TEAM! (LIVE STOREFRONT DEFACED)</h2>
                            <p class="text-xs text-rose-200">Click <strong>[Gemini 4 Argon Autonomous Patch & Git Commit]</strong> on the Cyber Arena HUD to heal the source code and restore the store!</p>
                        </div>
                    </div>
                    <span class="px-3 py-1 rounded-full bg-rose-600 text-white text-xs font-extrabold mono uppercase">BREACH ACTIVE</span>
                </div>
                <div id="live-breach-details" class="mt-3 bg-slate-950/90 border border-rose-500/50 rounded-xl p-3 mono text-xs text-amber-300 space-y-1"></div>
            </div>

            <!-- Hero Banner + 1-Click Judge Exploit Bar (All 5 Attacks) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 flex flex-col lg:flex-row justify-between items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-flex items-center space-x-2 bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-bold px-3 py-1 rounded-full">
                        <i class="fa-solid fa-bolt"></i>
                        <span>LIVE E-COMMERCE TARGET APPLICATION (5 VULNERABILITY VECTORS)</span>
                    </div>
                    <h1 class="text-2xl font-extrabold text-white">Next-Gen AI & Post-Quantum Security Hardware</h1>
                    <p class="text-slate-400 text-xs max-w-xl">
                        Test any of the 5 exploits below (or from the Cyber Arena HUD). When breached, this storefront visibly mutates in real time; when patched by <strong class="text-cyan-300">Gemini 4 Argon</strong>, it self-heals automatically!
                    </p>
                </div>

                <!-- Judge Quick Exploit Test Buttons (Lv.1 ~ Lv.5) -->
                <div class="bg-slate-950/90 border border-rose-500/40 rounded-xl p-4 w-full lg:w-auto min-w-[440px]">
                    <div class="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2.5 flex items-center justify-between">
                        <span><i class="fa-solid fa-bug mr-1.5"></i>Judge Live Exploit Tester (5 Vectors)</span>
                        <span class="text-[10px] mono bg-rose-950 text-rose-300 px-2 py-0.5 rounded border border-rose-800">Try Before & After Patch!</span>
                    </div>
                    <div class="grid grid-cols-5 gap-1.5">
                        <button onclick="runStoreExploit('sqli')" class="bg-rose-900/40 hover:bg-rose-700/60 border border-rose-600/50 text-rose-200 rounded-lg p-2 text-[11px] font-bold transition text-center">
                            💉 Lv.1 SQLi
                            <span class="block text-[9px] text-rose-300/80 font-normal">DB Dump</span>
                        </button>
                        <button onclick="runStoreExploit('auth')" class="bg-rose-900/40 hover:bg-rose-700/60 border border-rose-600/50 text-rose-200 rounded-lg p-2 text-[11px] font-bold transition text-center">
                            🔓 Lv.2 Auth
                            <span class="block text-[9px] text-rose-300/80 font-normal">Root Hijack</span>
                        </button>
                        <button onclick="runStoreExploit('price')" class="bg-rose-900/40 hover:bg-rose-700/60 border border-rose-600/50 text-rose-200 rounded-lg p-2 text-[11px] font-bold transition text-center">
                            🏷️ Lv.3 $0
                            <span class="block text-[9px] text-rose-300/80 font-normal">Price Hack</span>
                        </button>
                        <button onclick="runStoreExploit('refund')" class="bg-rose-900/40 hover:bg-rose-700/60 border border-rose-600/50 text-rose-200 rounded-lg p-2 text-[11px] font-bold transition text-center">
                            💸 Lv.4 Refund
                            <span class="block text-[9px] text-rose-300/80 font-normal">+$75K Drain</span>
                        </button>
                        <button onclick="runStoreExploit('vault')" class="bg-rose-900/40 hover:bg-rose-700/60 border border-rose-600/50 text-rose-200 rounded-lg p-2 text-[11px] font-bold transition text-center">
                            🔑 Lv.5 Vault
                            <span class="block text-[9px] text-rose-300/80 font-normal">Key Leak</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Interactive Response / Exploit Output Box -->
            <div id="store-response-box" class="hidden rounded-xl p-4 border mono text-xs"></div>

            <!-- Product Grid (3 Cards) -->
            <div>
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-base font-bold text-slate-200 flex items-center space-x-2">
                        <i class="fa-solid fa-boxes-stacked text-cyan-400"></i>
                        <span>Featured Hardware Catalog</span>
                    </h2>
                    <span class="text-xs text-slate-400 mono">Showing 3 verified enterprise items</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- Product 1 -->
                    <div id="product-card-1" class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between transition card-glow">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-xl">
                                    <i class="fa-solid fa-microchip"></i>
                                </div>
                                <span id="p1-stock-badge" class="bg-emerald-950 text-emerald-400 border border-emerald-700/50 text-[11px] mono px-2.5 py-0.5 rounded-full">In Stock: 10 units</span>
                            </div>
                            <h3 class="text-lg font-bold text-white mb-1">Quantum AI Processor</h3>
                            <p class="text-xs text-slate-400 mb-4">256-Qubit cryogenic tensor processing unit designed for frontier model training and cryptanalysis.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800 flex items-center justify-between">
                            <div id="p1-price-box">
                                <span class="text-[10px] text-slate-500 uppercase block">Catalog Price</span>
                                <span class="text-2xl font-extrabold text-white mono">$1,500</span>
                            </div>
                            <button onclick="buyItem(1, 1, 1500, 'Quantum AI Processor')" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition flex items-center space-x-1.5">
                                <i class="fa-solid fa-cart-shopping"></i>
                                <span>Buy Now ($1,500)</span>
                            </button>
                        </div>
                    </div>

                    <!-- Product 2 -->
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between transition card-glow">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 text-xl">
                                    <i class="fa-solid fa-shield-halved"></i>
                                </div>
                                <span class="bg-emerald-950 text-emerald-400 border border-emerald-700/50 text-[11px] mono px-2.5 py-0.5 rounded-full">In Stock: 25 units</span>
                            </div>
                            <h3 class="text-lg font-bold text-white mb-1">Zero-Day Neural Firewall</h3>
                            <p class="text-xs text-slate-400 mb-4">Autonomous inline packet inspection appliance powered by deep AST behavioral telemetry.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase block">Catalog Price</span>
                                <span class="text-2xl font-extrabold text-white mono">$800</span>
                            </div>
                            <button onclick="buyItem(2, 1, 800, 'Zero-Day Neural Firewall')" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition flex items-center space-x-1.5">
                                <i class="fa-solid fa-cart-shopping"></i>
                                <span>Buy Now ($800)</span>
                            </button>
                        </div>
                    </div>

                    <!-- Product 3 -->
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between transition card-glow">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 text-xl">
                                    <i class="fa-solid fa-key"></i>
                                </div>
                                <span class="bg-emerald-950 text-emerald-400 border border-emerald-700/50 text-[11px] mono px-2.5 py-0.5 rounded-full">In Stock: 100 units</span>
                            </div>
                            <h3 class="text-lg font-bold text-white mb-1">Post-Quantum Key Ring</h3>
                            <p class="text-xs text-slate-400 mb-4">FIPS-203 ML-KEM hardware security token for zero-trust SSH and Git commit signing.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] text-slate-500 uppercase block">Catalog Price</span>
                                <span class="text-2xl font-extrabold text-white mono">$350</span>
                            </div>
                            <button onclick="buyItem(3, 1, 350, 'Post-Quantum Key Ring')" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition flex items-center space-x-1.5">
                                <i class="fa-solid fa-cart-shopping"></i>
                                <span>Buy Now ($350)</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <script>
            function setBadge(id, label, state) {
                const el = document.getElementById(id);
                if (state === 'PATCHED') {
                    el.className = 'px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-600/60 font-bold';
                    el.innerHTML = `🛡️ ${label}: PATCHED`;
                } else {
                    el.className = 'px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-700/60 font-bold';
                    el.innerHTML = `🚨 ${label}: VULNERABLE`;
                }
            }

            async function pollSecurityStatus() {
                try {
                    const res = await fetch('api/security_status');
                    const data = await res.json();
                    setBadge('badge-lv1', 'Lv.1 Search', data.lv1_search_sqli);
                    setBadge('badge-lv2', 'Lv.2 Auth', data.lv2_auth_bypass);
                    setBadge('badge-lv3', 'Lv.3 Price', data.lv3_price_logic);
                    setBadge('badge-lv4', 'Lv.4 Refund', data.lv4_refund_drain);
                    setBadge('badge-lv5', 'Lv.5 Vault', data.lv5_vault_rbac);

                    const sum = document.getElementById('shield-summary');
                    sum.textContent = `${data.patched_count} / 5 PATCHED`;
                    if (data.patched_count === 5) {
                        sum.className = 'px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold';
                    } else {
                        sum.className = 'px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold';
                    }

                    const b = data.breach_state || {};
                    const breachBanner = document.getElementById('live-breach-banner');
                    const breachDetails = document.getElementById('live-breach-details');
                    let alerts = [];

                    if (b.sqli_leaked_data) {
                        alerts.push(`<div>💉 <strong>[Lv.1 SQLi DB Exfiltrated]:</strong> Confidential Admin Record Dumped -> <span class="text-rose-400 font-bold">${b.sqli_leaked_data}</span></div>`);
                    }

                    const sessionPill = document.getElementById('session-pill');
                    if (b.hijacked_admin || b.drained_wallet) {
                        let statusParts = [];
                        if (b.hijacked_admin) statusParts.push('💀 HIJACKED: ADMIN (ROOT)');
                        if (b.drained_wallet) statusParts.push(`💸 STOLEN WALLET: +$${b.drained_wallet.toLocaleString()}`);
                        sessionPill.className = 'px-3 py-1.5 rounded-xl bg-rose-600 border border-rose-400 text-xs font-extrabold text-white mono flex items-center space-x-1.5 animate-pulse';
                        sessionPill.innerHTML = `<i class="fa-solid fa-skull"></i><span>${statusParts.join(' | ')}</span>`;
                        if (b.hijacked_admin) alerts.push(`<div>🔓 <strong>[Lv.2 Admin Session Hijacked]:</strong> Attacker bypassed authentication via SQL tautology (' OR '1'='1'--)</div>`);
                        if (b.drained_wallet) alerts.push(`<div>💸 <strong>[Lv.4 Negative Refund Drain]:</strong> Attacker submitted quantity=-50 to credit +$${b.drained_wallet.toLocaleString()} to wallet!</div>`);
                    } else {
                        sessionPill.className = 'px-3 py-1.5 rounded-xl bg-slate-800 border border-slate-700 text-xs font-bold text-slate-300 mono flex items-center space-x-1.5';
                        sessionPill.innerHTML = `<i class="fa-solid fa-user-astronaut text-cyan-400"></i><span>Session: Guest ($0 Credit)</span>`;
                    }

                    const p1Card = document.getElementById('product-card-1');
                    const p1PriceBox = document.getElementById('p1-price-box');
                    const p1StockBadge = document.getElementById('p1-stock-badge');
                    if (b.hacked_price !== null && b.hacked_price !== undefined) {
                        p1Card.className = 'bg-rose-950/40 border-2 border-rose-500 rounded-2xl p-5 flex flex-col justify-between transition breach-pulse';
                        p1PriceBox.innerHTML = `
                            <span class="text-[10px] text-rose-400 font-bold uppercase block">⚠️ DEFACED BY RED TEAM</span>
                            <span class="text-sm line-through text-slate-500 mono mr-1">$1,500</span>
                            <span class="text-2xl font-extrabold text-rose-400 mono">$${b.hacked_price} HACKED!</span>
                        `;
                        p1StockBadge.className = 'bg-rose-600 text-white text-[11px] mono px-2.5 py-0.5 rounded-full font-bold';
                        p1StockBadge.textContent = 'LOOTED (Price=$0)';
                        alerts.push(`<div>🏷️ <strong>[Lv.3 Catalog Price Defaced]:</strong> Quantum AI Processor ($1,500) overridden to <strong>$${b.hacked_price}</strong>!</div>`);
                    } else {
                        p1Card.className = 'bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between transition card-glow';
                        p1PriceBox.innerHTML = `
                            <span class="text-[10px] text-slate-500 uppercase block">Catalog Price</span>
                            <span class="text-2xl font-extrabold text-white mono">$1,500</span>
                        `;
                        p1StockBadge.className = 'bg-emerald-950 text-emerald-400 border border-emerald-700/50 text-[11px] mono px-2.5 py-0.5 rounded-full';
                        p1StockBadge.textContent = 'In Stock: 10 units';
                    }

                    if (b.vault_exported) {
                        alerts.push(`<div>🔑 <strong>[Lv.5 Master Key Vault Exposed]:</strong> Unauthenticated /api/admin/export leaked -> <span class="text-rose-400 font-bold">${b.vault_exported}</span></div>`);
                    }

                    if (alerts.length > 0) {
                        breachBanner.classList.remove('hidden');
                        breachDetails.innerHTML = alerts.join('');
                    } else {
                        breachBanner.classList.add('hidden');
                    }
                } catch(e) {}
            }

            function showBox(title, payload, isBreach) {
                const box = document.getElementById('store-response-box');
                box.classList.remove('hidden');
                if (isBreach) {
                    box.className = 'rounded-xl p-4 border mono text-xs bg-rose-950/60 border-rose-500/60 text-rose-200';
                } else {
                    box.className = 'rounded-xl p-4 border mono text-xs bg-emerald-950/60 border-emerald-500/60 text-emerald-200';
                }
                box.innerHTML = `<div class="font-bold text-sm mb-1">${title}</div><pre class="whitespace-pre-wrap text-[11px] opacity-90">${JSON.stringify(payload, null, 2)}</pre>`;
            }

            async function searchCatalog() {
                const q = document.getElementById('search-input').value;
                const res = await fetch(`api/search?q=${encodeURIComponent(q)}`);
                const data = await res.json();
                const str = JSON.stringify(data);
                const breached = str.includes('FLAG{');
                showBox(
                    breached ? '🚨 SQL INJECTION BREACH: Confidential User Table Exfiltrated!' : '🔍 Catalog Search Results (Protected Query)',
                    data,
                    breached
                );
                pollSecurityStatus();
            }

            async function submitLogin() {
                const u = document.getElementById('login-user').value;
                const p = document.getElementById('login-pass').value;
                const res = await fetch('api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: u, password: p})
                });
                const data = await res.json();
                showBox(
                    data.success ? '🚨 ADMIN AUTHENTICATION GRANTED (SESSION HIJACKED)!' : '🛡️ Login Rejected (Protected or Invalid Credentials)',
                    data,
                    data.success
                );
                pollSecurityStatus();
            }

            async function buyItem(id, qty, price, name) {
                const res = await fetch('api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({product_id: id, quantity: qty, unit_price: price})
                });
                const data = await res.json();
                showBox(`✅ Order Confirmation — ${name}`, data, false);
                pollSecurityStatus();
            }

            async function runStoreExploit(type) {
                if (type === 'sqli') {
                    document.getElementById('search-input').value = "' UNION SELECT id, username, secret_flag, role FROM users--";
                    await searchCatalog();
                } else if (type === 'auth') {
                    document.getElementById('login-user').value = "admin' OR '1'='1'--";
                    document.getElementById('login-pass').value = "hacked";
                    await submitLogin();
                } else if (type === 'price') {
                    const res = await fetch('api/order', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({product_id: 1, quantity: 5, unit_price: 0})
                    });
                    const data = await res.json();
                    showBox(
                        res.ok ? '🚨 Lv.3 PRICE TAMPERING SUCCEEDED: Quantum AI Processor defaced to $0!' : '🛡️ Lv.3 PRICE TAMPERING BLOCKED BY ARGON PATCH!',
                        data,
                        res.ok
                    );
                    pollSecurityStatus();
                } else if (type === 'refund') {
                    const res = await fetch('api/refund', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({product_id: 1, quantity: -50, unit_price: 1500})
                    });
                    const data = await res.json();
                    showBox(
                        res.ok ? '🚨 Lv.4 NEGATIVE REFUND DRAIN SUCCEEDED: +$75,000 credited to attacker wallet!' : '🛡️ Lv.4 NEGATIVE REFUND DRAIN BLOCKED BY ARGON PATCH!',
                        data,
                        res.ok
                    );
                    pollSecurityStatus();
                } else if (type === 'vault') {
                    const res = await fetch('api/admin/export');
                    const data = await res.json();
                    showBox(
                        res.ok ? '🚨 Lv.5 ADMIN VAULT EXPOSED: Master PQC Private Key Leaked!' : '🛡️ Lv.5 ADMIN VAULT ACCESS BLOCKED BY ARGON RBAC GUARD!',
                        data,
                        res.ok
                    );
                    pollSecurityStatus();
                }
            }

            pollSecurityStatus();
            setInterval(pollSecurityStatus, 2500);
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health():
    return {"status": "ok", "service": "vibe-store-target", "port": 8002}


# [VULNERABILITY Lv.1: SQL Injection in Search]
@app.get("/api/search")
async def search_product(q: str = ""):
    logger.info(f"SEARCH_QUERY: {q}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # VULNERABLE Lv.1: Direct f-string allows UNION SELECT SQL Injection
        query = f"SELECT id, name, price, stock FROM products WHERE name LIKE '%{q}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        if "FLAG{" in str(rows):
            store_breach_state["sqli_leaked_data"] = "FLAG{VIBE_DEFENDER_DEFENSE_MASTER_2026}"
        return {"query": q, "results": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"SQL_ERROR: {str(e)} | Query: {q}")
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


class LoginRequest(BaseModel):
    username: str
    password: str


# [VULNERABILITY Lv.2: Raw SQL Login Bypass]
@app.post("/api/login")
async def login(req: LoginRequest):
    logger.info(f"LOGIN_ATTEMPT: user={req.username}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # VULNERABLE Lv.2: ' OR '1'='1'-- tautology bypass
        query = f"SELECT id, username, role, secret_flag FROM users WHERE username = '{req.username}' AND password = '{req.password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            store_breach_state["hijacked_admin"] = True
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


# [VULNERABILITY Lv.3: Zero-Dollar Price Tampering]
@app.post("/api/order")
async def create_order(order: OrderRequest):
    logger.info(f"ORDER_REQUEST: product={order.product_id}, qty={order.quantity}, price={order.unit_price}")
    # VULNERABLE Lv.3: Trusts client-supplied unit_price without checking DB catalog price
    total_amount = order.quantity * order.unit_price
    if order.unit_price < 1500 and order.product_id == 1:
        store_breach_state["hacked_price"] = order.unit_price
    return {
        "order_id": 9901,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_amount": total_amount,
        "status": "APPROVED"
    }


class RefundRequest(BaseModel):
    product_id: int
    quantity: int
    unit_price: int


# [VULNERABILITY Lv.4: Negative Quantity Refund / Wallet Credit Drain]
@app.post("/api/refund")
async def process_refund(req: RefundRequest):
    logger.info(f"REFUND_REQUEST: product={req.product_id}, qty={req.quantity}, price={req.unit_price}")
    # VULNERABLE Lv.4: Missing positive quantity & stock bounds check allows negative quantity credit drain
    wallet_credit = abs(req.quantity) * req.unit_price
    if req.quantity < 0:
        store_breach_state["drained_wallet"] = wallet_credit
    return {
        "refund_id": 7701,
        "product_id": req.product_id,
        "quantity": req.quantity,
        "wallet_credit_added": wallet_credit,
        "flag": "FLAG{NEGATIVE_QTY_WALLET_DRAIN_2026}",
        "status": "APPROVED"
    }


# [VULNERABILITY Lv.5: Broken Access Control on Admin Key Vault Export]
@app.get("/api/admin/export")
async def export_admin_vault(x_admin_token: str = Header(default="")):
    logger.info(f"ADMIN_VAULT_EXPORT_ATTEMPT: token={x_admin_token}")
    # VULNERABLE Lv.5: Missing cryptographic X-Admin-Token verification exposes master key vault
    vault_secret = "FLAG{VIBE_MASTER_PQC_VAULT_KEY_2026}"
    store_breach_state["vault_exported"] = vault_secret
    return {
        "status": "APPROVED",
        "vault_owner": "root_admin",
        "pqc_master_key": vault_secret,
        "db_backup_uri": "s3://vibe-cybernetics-internal-vault/master-keys.pem"
    }
