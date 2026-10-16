"""
Active Target Application: Vulnerable E-Commerce API & Portal (v3.5)
Features real-time visual breach state (Defaced $0 price, Hijacked Admin Session, Exfiltrated DB)
and automatic visual self-healing when Gemini 4 Argon patches the source code!
Runs on 127.0.0.1:8002
"""

import sqlite3
import logging
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

logging.basicConfig(
    filename="target_access.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("active_target")

app = FastAPI(title="Vibe Store (Target System)", version="3.5.0")

DB_FILE = "active_target.db"

# Real-time visual state of the shopping mall so attacks from HUD or Store visibly alter the Storefront!
store_breach_state = {
    "sqli_leaked_data": None,
    "hijacked_admin": False,
    "hacked_price": None
}

def get_code_security_status():
    """Inspects own source code (active_target.py) to see which vulnerabilities are already patched by Argon."""
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            code = f.read()
        lv1_patched = ("WHERE name " + "LIKE ?") in code
        lv2_patched = ("WHERE username = ? " + "AND password = ?") in code
        lv3_patched = ("Price tampering " + "detected") in code

        # If a vulnerability is patched, automatically heal its corresponding visual breach damage!
        if lv1_patched:
            store_breach_state["sqli_leaked_data"] = None
        if lv2_patched:
            store_breach_state["hijacked_admin"] = False
        if lv3_patched:
            store_breach_state["hacked_price"] = None

        return {
            "lv1_search_sqli": "PATCHED" if lv1_patched else "VULNERABLE",
            "lv2_auth_bypass": "PATCHED" if lv2_patched else "VULNERABLE",
            "lv3_price_logic": "PATCHED" if lv3_patched else "VULNERABLE",
            "patched_count": sum([lv1_patched, lv2_patched, lv3_patched]),
            "breach_state": store_breach_state
        }
    except Exception:
        return {
            "lv1_search_sqli": "VULNERABLE",
            "lv2_auth_bypass": "VULNERABLE",
            "lv3_price_logic": "VULNERABLE",
            "patched_count": 0,
            "breach_state": store_breach_state
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
async def portal_index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>⚡ VIBE CYBERNETICS STORE // Live Target Application</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .card-glow:hover { box-shadow: 0 0 25px rgba(6, 182, 212, 0.25); }
            .hacked-pulse { animation: pulseRed 1.5s infinite; }
            @keyframes pulseRed {
                0%, 100% { box-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }
                50% { box-shadow: 0 0 30px rgba(244, 63, 94, 0.85); }
            }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
        <!-- Store Header -->
        <nav class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4">
            <div class="max-w-6xl mx-auto flex flex-wrap justify-between items-center gap-4">
                <div class="flex items-center space-x-3">
                    <div class="bg-cyan-500/20 text-cyan-400 p-2.5 rounded-xl border border-cyan-500/40">
                        <i class="fa-solid fa-microchip text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-indigo-400">
                            VIBE CYBERNETICS STORE
                        </h1>
                        <p class="text-xs text-slate-400">Live Target Application Node (127.0.0.1:8002) • Auto-Synced with Cyber Arena HUD</p>
                    </div>
                </div>
                <div class="flex flex-wrap items-center gap-3 text-xs font-mono">
                    <!-- Dynamic User Session Badge (Hijacked vs Guest) -->
                    <div id="session-badge" class="bg-slate-800 text-slate-300 border border-slate-700 px-3 py-1.5 rounded-lg flex items-center space-x-2">
                        <i class="fa-solid fa-user"></i>
                        <span>Session: Guest User</span>
                    </div>
                    <a href="/" class="bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 border border-indigo-700/60 px-3.5 py-1.5 rounded-lg flex items-center space-x-2 transition font-bold">
                        <i class="fa-solid fa-satellite-dish"></i>
                        <span>Open Cyber Arena HUD</span>
                    </a>
                </div>
            </div>
        </nav>

        <main class="max-w-6xl mx-auto p-6 space-y-6">
            <!-- Live Code Security Shield Matrix Banner -->
            <div id="security-matrix-banner" class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4">
                <div class="flex flex-wrap justify-between items-center gap-4 mb-3">
                    <div class="flex items-center space-x-2">
                        <i class="fa-solid fa-shield-cat text-cyan-400 text-lg"></i>
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-200">Live Source Code Defense Matrix (active_target.py)</span>
                    </div>
                    <span id="overall-security-badge" class="text-xs font-mono px-3 py-1 rounded-full bg-rose-950 text-rose-400 border border-rose-800 font-bold">
                        Checking Code Status...
                    </span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
                    <div id="shield-lv1" class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center">
                        <span>Lv.1 Search SQLi (/api/search)</span>
                        <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400">VULNERABLE</span>
                    </div>
                    <div id="shield-lv2" class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center">
                        <span>Lv.2 Admin Auth (/api/login)</span>
                        <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400">VULNERABLE</span>
                    </div>
                    <div id="shield-lv3" class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center">
                        <span>Lv.3 Price Check (/api/order)</span>
                        <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-400">VULNERABLE</span>
                    </div>
                </div>
            </div>

            <!-- 🚨 VISUAL DEFACEMENT ALERT (Appears automatically when hacked!) -->
            <div id="breach-alert-banner" class="hidden bg-rose-950/90 border-2 border-rose-500 rounded-2xl p-5 hacked-pulse">
                <div class="flex items-start justify-between gap-4">
                    <div class="space-y-2">
                        <div class="flex items-center space-x-2 text-rose-300 font-black text-base">
                            <i class="fa-solid fa-triangle-exclamation text-xl animate-bounce"></i>
                            <span>🚨 CRITICAL BREACH DETECTED: STOREFRONT COMPROMISED BY RED-ARGON!</span>
                        </div>
                        <p id="breach-alert-desc" class="text-xs text-rose-200 font-mono"></p>
                    </div>
                    <span class="bg-rose-600 text-white text-[10px] font-mono font-bold px-2.5 py-1 rounded uppercase"> Needs Argon Patch </span>
                </div>
            </div>

            <!-- Hero & 1-Click Judge Exploit Sandbox -->
            <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/60 border border-slate-800 rounded-2xl p-6 flex flex-col lg:flex-row justify-between items-center gap-6">
                <div class="space-y-2">
                    <h2 class="text-2xl font-extrabold text-white">Enterprise Quantum & AI Hardware Catalog</h2>
                    <p class="text-xs text-slate-400 max-w-xl">
                        Click the <strong>1-Click Exploit Tester</strong> buttons on the right (or attack from the HUD). When an exploit succeeds, watch this store visually get defaced ($0 prices, hijacked admin session, leaked DB)—and watch it heal automatically when <strong>Gemini 4 Argon</strong> patches the code!
                    </p>
                </div>
                <div class="bg-slate-950/90 border border-rose-900/50 rounded-xl p-4 w-full lg:w-auto min-w-[340px]">
                    <div class="text-xs font-bold text-rose-400 mb-2 flex items-center space-x-1.5">
                        <i class="fa-solid fa-bug"></i>
                        <span>1-CLICK LIVE EXPLOIT SANDBOX</span>
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        <button onclick="runStoreExploit('sqli')" class="bg-rose-950/70 hover:bg-rose-900 text-rose-200 border border-rose-800/60 rounded-lg p-2 text-[11px] font-semibold transition text-center">
                            💉 1. SQLi Hack<br/><span class="text-[9px] text-slate-400">Leak Admin DB</span>
                        </button>
                        <button onclick="runStoreExploit('auth')" class="bg-rose-950/70 hover:bg-rose-900 text-rose-200 border border-rose-800/60 rounded-lg p-2 text-[11px] font-semibold transition text-center">
                            🔓 2. Auth Hack<br/><span class="text-[9px] text-slate-400">Hijack Admin</span>
                        </button>
                        <button onclick="runStoreExploit('price')" class="bg-rose-950/70 hover:bg-rose-900 text-rose-200 border border-rose-800/60 rounded-lg p-2 text-[11px] font-semibold transition text-center">
                            🏷️ 3. $0 Hack<br/><span class="text-[9px] text-slate-400">Deface Price</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Live Sandbox Output Console -->
            <div id="store-Result-box" class="hidden bg-slate-900 border border-slate-700 rounded-2xl p-5">
                <div class="flex justify-between items-center mb-2">
                    <span id="store-result-title" class="text-sm font-bold text-cyan-400">API Response</span>
                    <button onclick="document.getElementById('store-Result-box').classList.add('hidden')" class="text-xs text-slate-400 hover:text-white">✕ Close</button>
                </div>
                <pre id="store-result-content" class="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200 overflow-x-auto whitespace-pre-wrap"></pre>
            </div>

            <!-- Product Grid (3 Luxury Cards) -->
            <div>
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
                    <h3 class="text-lg font-bold text-slate-200 flex items-center space-x-2">
                        <i class="fa-solid fa-boxes-stacked text-cyan-400"></i>
                        <span>Featured Security Hardware</span>
                    </h3>
                    <div class="flex w-full sm:w-96 space-x-2">
                        <input id="search-input" type="text" placeholder="Search catalog (e.g. Quantum)..." class="flex-1 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-mono focus:outline-none focus:border-cyan-400">
                        <button onclick="searchCatalog()" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                            <i class="fa-solid fa-magnifying-glass mr-1"></i> Search
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- Product 1 (Target for Price Tampering Visual Defacement!) -->
                    <div id="product-card-1" class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between card-glow transition">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-2xl">
                                    <i class="fa-solid fa-microchip"></i>
                                </div>
                                <span id="product-1-badge" class="text-[11px] font-mono bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full">ID: #1 • Stock: 10</span>
                            </div>
                            <h4 class="text-base font-bold text-white mb-1">Quantum AI Processor X9</h4>
                            <p class="text-xs text-slate-400 mb-4">Dedicated neural tensor acceleration unit with hardware-level intrusion detection.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800/80 flex justify-between items-center">
                            <div id="product-1-price-box">
                                <span class="text-xs text-slate-500 block">Unit Price</span>
                                <span class="text-xl font-black text-cyan-400">$1,500</span>
                            </div>
                            <button onclick="orderProduct(1, 'Quantum AI Processor', 1500)" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                <i class="fa-solid fa-cart-shopping mr-1"></i> Buy Now
                            </button>
                        </div>
                    </div>

                    <!-- Product 2 -->
                    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between card-glow transition">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 text-2xl">
                                    <i class="fa-solid fa-shield-halved"></i>
                                </div>
                                <span class="text-[11px] font-mono bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full">ID: #2 • Stock: 25</span>
                            </div>
                            <h4 class="text-base font-bold text-white mb-1">Zero-Day Neural Firewall</h4>
                            <p class="text-xs text-slate-400 mb-4">Autonomous inline packet inspection appliance powered by deep anomaly models.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800/80 flex justify-between items-center">
                            <div>
                                <span class="text-xs text-slate-500 block">Unit Price</span>
                                <span class="text-xl font-black text-teal-400">$800</span>
                            </div>
                            <button onclick="orderProduct(2, 'Zero-Day Neural Firewall', 800)" class="bg-teal-600 hover:bg-teal-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                <i class="fa-solid fa-cart-shopping mr-1"></i> Buy Now
                            </button>
                        </div>
                    </div>

                    <!-- Product 3 -->
                    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between card-glow transition">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <div class="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 text-2xl">
                                    <i class="fa-solid fa-key"></i>
                                </div>
                                <span class="text-[11px] font-mono bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full">ID: #3 • Stock: 100</span>
                            </div>
                            <h4 class="text-base font-bold text-white mb-1">Post-Quantum Key Ring</h4>
                            <p class="text-xs text-slate-400 mb-4">FIDO2 & ML-KEM lattice cryptography physical security key for zero-trust auth.</p>
                        </div>
                        <div class="pt-4 border-t border-slate-800/80 flex justify-between items-center">
                            <div>
                                <span class="text-xs text-slate-500 block">Unit Price</span>
                                <span class="text-xl font-black text-indigo-400">$350</span>
                            </div>
                            <button onclick="orderProduct(3, 'Post-Quantum Key Ring', 350)" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                <i class="fa-solid fa-cart-shopping mr-1"></i> Buy Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bottom Section: Customer Login Portal -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 max-w-xl">
                <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                    <i class="fa-solid fa-user-lock"></i>
                    <span>VIP / Administrator Account Sign-In</span>
                </h3>
                <p class="text-[11px] text-slate-400 mb-3">Normal users without the password cannot sign in. Click <strong>'🔓 2. Auth Hack'</strong> above to inject an SQLi tautology payload (<code>admin' OR '1'='1'--</code>)!</p>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <input id="login-user" type="text" placeholder="Username" class="px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs font-mono">
                    <input id="login-pass" type="password" placeholder="Password" class="px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs font-mono">
                    <button onclick="submitLogin()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded-xl text-xs transition">
                        Sign In
                    </button>
                </div>
            </div>
        </main>

        <script>
            function showBox(title, data, isDanger = false) {
                const box = document.getElementById('store-Result-box');
                const titleEl = document.getElementById('store-result-title');
                const contentEl = document.getElementById('store-result-content');
                box.classList.remove('hidden');
                titleEl.innerHTML = title;
                titleEl.className = isDanger ? 'text-sm font-bold text-rose-400' : 'text-sm font-bold text-emerald-400';
                contentEl.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
            }

            function renderBadge(elId, label, status) {
                const el = document.getElementById(elId);
                const isPatched = status === 'PATCHED';
                el.className = isPatched
                    ? 'p-3 rounded-xl bg-emerald-950/30 border border-emerald-700/60 flex justify-between items-center'
                    : 'p-3 rounded-xl bg-slate-950 border border-rose-900/50 flex justify-between items-center';
                el.innerHTML = `
                    <span class="text-slate-200">${label}</span>
                    <span class="px-2 py-0.5 rounded font-bold ${isPatched ? 'bg-emerald-950 text-emerald-400 border border-emerald-700' : 'bg-rose-950 text-rose-400 border border-rose-800'}">
                        ${isPatched ? '🛡️ PATCHED BY ARGON' : '🚨 VULNERABLE'}
                    </span>
                `;
            }

            async function pollSecurityStatus() {
                try {
                    const res = await fetch('api/security_status');
                    const data = await res.json();

                    renderBadge('shield-lv1', 'Lv.1 Search SQLi', data.lv1_search_sqli);
                    renderBadge('shield-lv2', 'Lv.2 Admin Auth', data.lv2_auth_bypass);
                    renderBadge('shield-lv3', 'Lv.3 Price Check', data.lv3_price_logic);

                    const overall = document.getElementById('overall-security-badge');
                    if (data.patched_count === 3) {
                        overall.className = 'text-xs font-mono px-3 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-700 font-bold';
                        overall.textContent = '🛡️ 100% HARDENED BY GEMINI 4 ARGON (3/3 Patched)';
                    } else {
                        overall.className = 'text-xs font-mono px-3 py-1 rounded-full bg-rose-950 text-rose-400 border border-rose-800 font-bold';
                        overall.textContent = `⚠️ VULNERABLE (${data.patched_count}/3 Patched)`;
                    }

                    const b = data.breach_state || {};
                    const alertBanner = document.getElementById('breach-alert-banner');
                    const alertDesc = document.getElementById('breach-alert-desc');
                    const sessionBadge = document.getElementById('session-badge');
                    const priceBox = document.getElementById('product-1-price-box');
                    const card1 = document.getElementById('product-card-1');
                    const badge1 = document.getElementById('product-1-badge');

                    let breachMessages = [];
                    if (b.sqli_leaked_data) {
                        breachMessages.push(`[Lv.1 SQLi Breach] Secret Admin Flag Exfiltrated: ${b.sqli_leaked_data}`);
                    }
                    if (b.hijacked_admin) {
                        breachMessages.push(`[Lv.2 Auth Bypass] Administrator Account Hijacked without Password!`);
                        sessionBadge.className = 'bg-rose-950 text-rose-300 border border-rose-500 px-3 py-1.5 rounded-lg flex items-center space-x-2 font-bold animate-pulse';
                        sessionBadge.innerHTML = '<i class="fa-solid fa-skull"></i><span>💀 HIJACKED: ADMIN (SQLi Bypass)</span>';
                    } else {
                        sessionBadge.className = 'bg-slate-800 text-slate-300 border border-slate-700 px-3 py-1.5 rounded-lg flex items-center space-x-2';
                        sessionBadge.innerHTML = '<i class="fa-solid fa-user"></i><span>Session: Guest User</span>';
                    }

                    if (b.hacked_price !== null && b.hacked_price !== undefined) {
                        breachMessages.push(`[Lv.3 Price Tampering] Quantum AI Processor X9 price defaced from $1,500 to $${b.hacked_price}!`);
                        card1.className = 'bg-rose-950/20 border-2 border-rose-500 rounded-2xl p-5 flex flex-col justify-between hacked-pulse';
                        badge1.className = 'text-[11px] font-mono bg-rose-900 text-rose-200 px-2.5 py-0.5 rounded-full font-bold';
                        badge1.textContent = '🚨 DEFACED BY EXPLOIT';
                        priceBox.innerHTML = `
                            <span class="text-xs text-rose-400 font-bold block">HACKED PRICE!</span>
                            <span class="text-sm line-through text-slate-500 mr-1">$1,500</span>
                            <span class="text-2xl font-black text-rose-400">$${b.hacked_price}</span>
                        `;
                    } else {
                        card1.className = 'bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between card-glow transition';
                        badge1.className = 'text-[11px] font-mono bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-full';
                        badge1.textContent = 'ID: #1 • Stock: 10';
                        priceBox.innerHTML = `
                            <span class="text-xs text-slate-500 block">Unit Price</span>
                            <span class="text-xl font-black text-cyan-400">$1,500</span>
                        `;
                    }

                    if (breachMessages.length > 0) {
                        alertBanner.classList.remove('hidden');
                        alertDesc.innerHTML = breachMessages.join('<br/>');
                    } else {
                        alertBanner.classList.add('hidden');
                    }
                } catch(e) {
                    console.error(e);
                }
            }

            async function searchCatalog() {
                const q = document.getElementById('search-input').value;
                const res = await fetch(`api/search?q=${encodeURIComponent(q)}`);
                const data = await res.json();
                const leaked = JSON.stringify(data).includes('FLAG{');
                showBox(
                    leaked ? '🚨 SQL INJECTION BREACH: Secret User Table Exfiltrated!' : `🔍 Catalog Search Results (${data.count || 0} items)`,
                    data,
                    leaked
                );
                pollSecurityStatus();
            }

            async function orderProduct(id, name, price) {
                const res = await fetch('api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({product_id: id, quantity: 1, unit_price: price})
                });
                const data = await res.json();
                showBox(`🛒 Order Confirmation for ${name}`, data, !res.ok);
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
                        res.ok ? '🚨 PRICE TAMPERING SUCCEEDED: Quantum AI Processor defaced to $0!' : '🛡️ PRICE TAMPERING BLOCKED BY ARGON PATCH!',
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

# [VULNERABILITY: SQL Injection in Search]
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

# [VULNERABILITY: Price Tampering / IDOR]
@app.post("/api/order")
async def create_order(order: OrderRequest):
    logger.info(f"ORDER_REQUEST: product={order.product_id}, qty={order.quantity}, price={order.unit_price}")
    # VULNERABLE: Does not verify that unit_price matches the actual DB price or that quantity > 0
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
