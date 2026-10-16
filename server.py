"""
Vibe Defender Cyber Arena HUD & Orchestrator
Coordinates Red Server (8003), Blue Server (8004), Target App (8002).
Provides Web HUD on 127.0.0.1:8080, Reverse Proxy for Target Portal,
and Telemetry Endpoints for Flutter-Firebase integration.
"""

import os
import subprocess
import requests
import httpx
from datetime import datetime
from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Vibe Defender Cyber Arena HUD", version="2.1.0")

TARGET_HOST = "http://127.0.0.1:8002"
RED_HOST = "http://127.0.0.1:8003"
BLUE_HOST = "http://127.0.0.1:8004"

telemetry_events = []
arena_state = {
    "last_attacked_level": 0,
    "last_patch_info": None
}

def add_event(source: str, level: str, message: str, details: dict = None):
    event = {
        "id": len(telemetry_events) + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "source": source,
        "level": level,
        "message": message,
        "details": details or {}
    }
    telemetry_events.append(event)
    if len(telemetry_events) > 100:
        telemetry_events.pop(0)
    return event

@app.get("/", response_class=HTMLResponse)
async def hud_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛡️ Vibe Defender - Autonomous Cyber Arena HUD</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .glow-cyan { box-shadow: 0 0 20px rgba(6, 182, 212, 0.35); }
            .glow-rose { box-shadow: 0 0 20px rgba(244, 63, 94, 0.35); }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
        <!-- Top Nav -->
        <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur px-6 py-4 flex flex-wrap justify-between items-center gap-4 sticky top-0 z-50">
            <div class="flex items-center space-x-3">
                <div class="bg-cyan-500/20 text-cyan-400 p-2.5 rounded-xl border border-cyan-500/40 glow-cyan">
                    <i class="fa-solid fa-shield-halved text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-indigo-400">
                        VIBE DEFENDER // AUTONOMOUS CYBER ARENA
                    </h1>
                    <p class="text-xs text-slate-400">Powered by Gemini 4 Argon (Interactions API) • GCE Zero-Inbound Protected Architecture</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-3 text-xs font-mono">
                <button onclick="resetArena()" class="bg-rose-950/80 hover:bg-rose-900 text-rose-300 border border-rose-700/60 px-3.5 py-1.5 rounded-lg flex items-center space-x-2 transition font-bold shadow-lg shadow-rose-950/50">
                    <i class="fa-solid fa-arrow-rotate-left"></i>
                    <span>⚡ Reset Arena</span>
                </button>
                <a href="/portal/" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 px-3 py-1.5 rounded-lg border border-slate-700 flex items-center space-x-1.5 transition">
                    <i class="fa-solid fa-store"></i>
                    <span>Target Portal (E-Commerce)</span>
                </a>
                <span class="bg-emerald-950 text-emerald-400 border border-emerald-800/80 px-3 py-1 rounded-lg flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>ALL NODES ONLINE</span>
                </span>
            </div>
        </header>

        <main class="max-w-7xl mx-auto p-6 space-y-6">
            <!-- Grid Row 1: Dual Control Nodes (Red vs Blue) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Red Team Adversary Node -->
                <div class="bg-slate-900/90 border border-rose-900/40 rounded-2xl p-5 glow-rose relative flex flex-col justify-between">
                    <div>
                        <div class="flex justify-between items-center pb-3 border-b border-rose-900/30 mb-4">
                            <div class="flex items-center space-x-2 text-rose-400 font-bold">
                                <i class="fa-solid fa-skull-crossbones text-lg"></i>
                                <span class="tracking-wider">RED ADVERSARY // Port 8003</span>
                            </div>
                            <span class="text-[11px] font-mono bg-rose-950/80 text-rose-400 px-2.5 py-0.5 rounded-full border border-rose-800">
                                Argon thinking_level="medium"
                            </span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">Generates polymorphic exploit payloads against target e-commerce endpoints:</p>
                        <div class="grid grid-cols-3 gap-2.5 mb-4">
                            <button onclick="triggerAttack('sqli_search', 1)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-xl p-3 text-xs font-semibold text-center transition flex flex-col items-center justify-center space-y-1">
                                <span class="text-sm">💉 SQLi Search</span>
                                <span class="text-[10px] text-slate-400">Data Exfiltration (Lv.1)</span>
                            </button>
                            <button onclick="triggerAttack('auth_bypass', 2)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-xl p-3 text-xs font-semibold text-center transition flex flex-col items-center justify-center space-y-1">
                                <span class="text-sm">🔓 Auth Bypass</span>
                                <span class="text-[10px] text-slate-400">Admin Bypass (Lv.2)</span>
                            </button>
                            <button onclick="triggerAttack('price_tampering', 3)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-xl p-3 text-xs font-semibold text-center transition flex flex-col items-center justify-center space-y-1">
                                <span class="text-sm">🏷️ Price Exploit</span>
                                <span class="text-[10px] text-slate-400">Logic Tampering (Lv.3)</span>
                            </button>
                        </div>
                    </div>
                    <div id="red-result" class="bg-slate-950/90 p-3.5 rounded-xl border border-slate-800/80 font-mono text-xs text-rose-300 min-h-[90px] overflow-auto">
                        [Red Team Ready] Select an attack scenario (Lv.1 ~ Lv.3) to launch an exploit.
                    </div>
                </div>

                <!-- Blue Team Self-Healing Node -->
                <div class="bg-slate-900/90 border border-cyan-900/40 rounded-2xl p-5 glow-cyan relative flex flex-col justify-between">
                    <div>
                        <div class="flex justify-between items-center pb-3 border-b border-cyan-900/30 mb-4">
                            <div class="flex items-center space-x-2 text-cyan-400 font-bold">
                                <i class="fa-solid fa-shield-virus text-lg"></i>
                                <span class="tracking-wider">BLUE DEFENDER // Port 8004</span>
                            </div>
                            <span class="text-[11px] font-mono bg-cyan-950/80 text-cyan-400 px-2.5 py-0.5 rounded-full border border-cyan-800">
                                Argon thinking_level="high"
                            </span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">Deep telemetry reasoning, automated code refactoring & live Git commit:</p>
                        <div class="flex space-x-3 mb-4">
                            <button onclick="triggerDefensePatch()" class="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-4 rounded-xl text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-cyan-600/30">
                                <i class="fa-solid fa-wand-magic-sparkles"></i>
                                <span>Gemini 4 Argon Autonomous Patch & Git Commit</span>
                            </button>
                            <button onclick="refreshDiff()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-3 rounded-xl text-xs font-mono border border-slate-700 transition" title="Refresh Git Diff">
                                <i class="fa-solid fa-rotate"></i>
                            </button>
                        </div>
                    </div>
                    <div id="blue-result" class="bg-slate-950/90 p-3.5 rounded-xl border border-slate-800/80 font-mono text-xs text-cyan-300 min-h-[90px] overflow-auto">
                        [Blue Team Ready] Monitoring telemetry stream for breach events...
                    </div>
                </div>
            </div>

            <!-- Grid Row 2: Dual Log Stream (Packet Log vs Visual Before/After Code Evolution) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Left: Real-Time Adversary & Breach Telemetry -->
                <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col">
                    <div class="flex justify-between items-center pb-3 border-b border-slate-800 mb-3">
                        <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                            <i class="fa-solid fa-terminal text-rose-400"></i>
                            <span>1. Real-Time Adversary & Breach Telemetry Stream</span>
                        </h3>
                        <span class="text-[11px] font-mono text-slate-500">target_access.log</span>
                    </div>
                    <div id="packet-log-stream" class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-xs text-slate-300 space-y-1.5 h-80 overflow-y-auto">
                        <div class="text-slate-500">[Idle] Waiting for adversary attack stream...</div>
                    </div>
                </div>

                <!-- Right: Visual Before vs After Code Evolution Viewer -->
                <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col">
                    <div class="flex justify-between items-center pb-3 border-b border-slate-800 mb-3">
                        <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                            <i class="fa-solid fa-code-compare text-teal-400"></i>
                            <span>2. Live Source Code Evolution (Before vs. After)</span>
                        </h3>
                        <span class="text-[11px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                            active_target.py • uvicorn hot-reload
                        </span>
                    </div>
                    <div id="diff-viewer" class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-xs h-80 overflow-y-auto space-y-3">
                        <div class="text-slate-500">Click an Attack button and then 'Autonomous Patch' to see the exact lines of code evolve in real time.</div>
                    </div>
                </div>
            </div>

            <!-- Grid Row 3: Git Commit Timeline -->
            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center space-x-2">
                    <i class="fa-solid fa-code-branch text-indigo-400"></i>
                    <span>3. Git Commit Timeline (Immutable History)</span>
                </h3>
                <div id="git-log" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 text-xs font-mono">
                    <div class="text-slate-500">Loading commit timeline...</div>
                </div>
            </div>
        </main>

        <script>
            let currentAttackLevel = 0;

            function escapeHtml(str) {
                return (str || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
            }

            function renderColorDiff(rawDiff, patchInfo) {
                const viewer = document.getElementById('diff-viewer');
                let html = '';

                if (patchInfo && patchInfo.before_code && patchInfo.after_code) {
                    html += `
                        <div class="mb-3">
                            <div class="text-[11px] font-bold text-cyan-400 mb-1.5 flex items-center justify-between">
                                <span>📍 Target Location: ${escapeHtml(patchInfo.target_endpoint || 'active_target.py')}</span>
                                <span>Commit: ${escapeHtml(patchInfo.commit_hash || 'HEAD')}</span>
                            </div>
                            <div class="bg-rose-950/40 border-l-4 border-rose-500 p-2.5 rounded-r-lg mb-2">
                                <div class="text-[10px] font-bold text-rose-400 uppercase mb-1">❌ BEFORE (Vulnerable Code Removed)</div>
                                <pre class="text-rose-200 whitespace-pre-wrap text-[11px]">- ${escapeHtml(patchInfo.before_code)}</pre>
                            </div>
                            <div class="bg-emerald-950/40 border-l-4 border-emerald-500 p-2.5 rounded-r-lg">
                                <div class="text-[10px] font-bold text-emerald-400 uppercase mb-1">✅ AFTER (Patched by Gemini 4 Argon)</div>
                                <pre class="text-emerald-200 whitespace-pre-wrap text-[11px]">+ ${escapeHtml(patchInfo.after_code)}</pre>
                            </div>
                        </div>
                        <div class="border-t border-slate-800 pt-2 text-[10px] text-slate-500 uppercase font-bold">Raw Git Diff Output:</div>
                    `;
                }

                if (rawDiff && !rawDiff.includes('No uncommitted')) {
                    const lines = rawDiff.split('\\n');
                    const formattedLines = lines.map(line => {
                        if (line.startsWith('---') || line.startsWith('+++') || line.startsWith('diff ') || line.startsWith('index ')) {
                            return `<div class="text-slate-500">${escapeHtml(line)}</div>`;
                        } else if (line.startsWith('-')) {
                            return `<div class="bg-rose-950/70 text-rose-300 px-2 py-0.5 border-l-2 border-rose-500">${escapeHtml(line)}</div>`;
                        } else if (line.startsWith('+')) {
                            return `<div class="bg-emerald-950/70 text-emerald-300 px-2 py-0.5 border-l-2 border-emerald-500">${escapeHtml(line)}</div>`;
                        } else if (line.startsWith('@@')) {
                            return `<div class="text-indigo-400 font-bold mt-1">${escapeHtml(line)}</div>`;
                        }
                        return `<div class="text-slate-400">${escapeHtml(line)}</div>`;
                    }).join('');
                    html += `<div class="space-y-0.5">${formattedLines}</div>`;
                } else if (!html) {
                    html = `<div class="text-slate-500">No code changes yet. Launch an attack and click 'Autonomous Patch' to watch the code evolve!</div>`;
                }

                viewer.innerHTML = html;
            }

            async function triggerAttack(scenario, level) {
                currentAttackLevel = level;
                const redBox = document.getElementById('red-result');
                redBox.innerHTML = '<span class="text-slate-400">Generating Gemini 4 Argon payload and dispatching exploit...</span>';
                try {
                    const res = await fetch(`/api/attack?scenario=${scenario}&level=${level}`, { method: 'POST' });
                    const data = await res.json();
                    let html = `<div><strong>[Attack Result]</strong> ${data.breached ? '<span class="text-rose-400 font-bold">🚨 TARGET BREACHED (VULNERABLE)</span>' : '<span class="text-emerald-400 font-bold">🛡️ ATTACK BLOCKED (PROTECTED BY ARGON PATCH)</span>'}</div>`;
                    if (data.flag) {
                        html += `<div class="text-amber-400 font-bold mt-1">🚩 Flag Exfiltrated: ${data.flag}</div>`;
                    }
                    html += `<div class="text-slate-400 text-[11px] mt-1">${data.payload?.description || ''}</div>`;
                    redBox.innerHTML = html;
                    refreshLogs();
                } catch(e) {
                    redBox.innerHTML = `<span class="text-red-400">Attack request error: ${e}</span>`;
                }
            }

            async function triggerDefensePatch() {
                const blueBox = document.getElementById('blue-result');
                blueBox.innerHTML = '<span class="text-slate-400">Gemini 4 Argon (High) analyzing AST and synthesizing security patch...</span>';
                try {
                    const res = await fetch(`/api/defense/patch?round_num=${currentAttackLevel}`, { method: 'POST' });
                    const data = await res.json();
                    if (data.status === 'patched') {
                        blueBox.innerHTML = `<div><strong>[Patch Applied]</strong> ${data.description}</div><div class="text-xs text-emerald-400 mt-1">Git Commit: ${data.commit_hash} • Target: ${data.target_endpoint}</div>`;
                    } else {
                        blueBox.innerHTML = `<div><strong>[Info]</strong> ${data.message}</div>`;
                    }
                    await refreshDiff(data);
                    refreshGitLog();
                    refreshLogs();
                } catch(e) {
                    blueBox.innerHTML = `<span class="text-red-400">Patch error: ${e}</span>`;
                }
            }

            async function resetArena() {
                if(!confirm('Reset the cyber arena to the vulnerable baseline state?')) return;
                try {
                    const res = await fetch('/api/arena/reset', { method: 'POST' });
                    const data = await res.json();
                    currentAttackLevel = 0;
                    document.getElementById('diff-viewer').innerHTML = '<div class="text-amber-300 font-bold">⚡ Arena Reset to Vulnerable Baseline! All 3 vulnerabilities are active again.</div>';
                    refreshGitLog();
                    refreshLogs();
                    document.getElementById('red-result').innerText = '[Red Team Ready] Arena restored to vulnerable baseline.';
                    document.getElementById('blue-result').innerText = '[Blue Team Ready] Waiting for adversary attacks.';
                } catch(e) {
                    alert('Reset error: ' + e);
                }
            }

            async function refreshDiff(patchData = null) {
                try {
                    const res = await fetch('/api/git/diff');
                    const data = await res.json();
                    renderColorDiff(data.diff, patchData || data.last_patch);
                } catch(e) {
                    console.error(e);
                }
            }

            async function refreshGitLog() {
                try {
                    const res = await fetch('/api/git/history');
                    const data = await res.json();
                    const container = document.getElementById('git-log');
                    if(data.commits && data.commits.length > 0) {
                        container.innerHTML = data.commits.map(c => `
                            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800/80">
                                <div class="text-cyan-400 font-bold mb-1">${c.hash}</div>
                                <div class="text-slate-300 truncate text-[11px]">${c.message}</div>
                                <div class="text-[10px] text-slate-500 mt-1">${c.time}</div>
                            </div>
                        `).join('');
                    } else {
                        container.innerHTML = '<div class="text-slate-500">No commits found</div>';
                    }
                } catch(e) {
                    console.error(e);
                }
            }

            async function refreshLogs() {
                try {
                    const res = await fetch('/api/telemetry/feed');
                    const data = await res.json();
                    const stream = document.getElementById('packet-log-stream');
                    if(data.events && data.events.length > 0) {
                        stream.innerHTML = data.events.slice().reverse().map(ev => {
                            let color = 'text-slate-300';
                            if(ev.level === 'BREACH') color = 'text-rose-400 font-bold';
                            if(ev.level === 'PATCH') color = 'text-cyan-300 font-bold';
                            if(ev.level === 'RESET') color = 'text-amber-300 font-bold';
                            return `<div class="${color}">[${ev.timestamp}] [${ev.source}] ${ev.message}</div>`;
                        }).join('');
                    }
                } catch(e) {
                    console.error(e);
                }
            }

            refreshGitLog();
            refreshDiff();
            refreshLogs();
            setInterval(refreshLogs, 4000);
        </script>
    </body>
    </html>
    """

@app.api_route("/portal/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def portal_proxy(request: Request, path: str = ""):
    url = f"{TARGET_HOST}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"
    
    async with httpx.AsyncClient() as client:
        try:
            req_body = await request.body()
            res = await client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                content=req_body,
                timeout=10.0
            )
            return Response(content=res.content, status_code=res.status_code, headers=dict(res.headers))
        except Exception as e:
            return JSONResponse(status_code=502, content={"error": f"Target service unavailable: {str(e)}"})

@app.post("/api/attack")
async def trigger_attack(scenario: str = "sqli_search", level: int = 1):
    arena_state["last_attacked_level"] = level
    try:
        res = requests.post(f"{RED_HOST}/attack?scenario={scenario}&level={level}", timeout=10)
        data = res.json()
        log_lvl = "BREACH" if data.get("breached") else "INFO"
        add_event("RED_AGENT", log_lvl, f"Scenario: {scenario} (Lv.{level}) -> Breached: {data.get('breached')}", data)
        return data
    except Exception as e:
        add_event("RED_AGENT", "ERROR", f"Attack request failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/defense/patch")
async def trigger_patch(round_num: int = 0):
    target_round = round_num if round_num > 0 else arena_state.get("last_attacked_level", 0)
    try:
        res = requests.post(f"{BLUE_HOST}/patch?round_num={target_round}", timeout=20)
        data = res.json()
        if data.get("status") == "patched":
            arena_state["last_patch_info"] = data
            add_event("BLUE_AGENT", "PATCH", f"Auto-patch committed ({data.get('commit_hash')}): {data.get('description')}", data)
        return data
    except Exception as e:
        add_event("BLUE_AGENT", "ERROR", f"Patch request failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/arena/reset")
async def trigger_reset():
    try:
        res = requests.post(f"{BLUE_HOST}/reset", timeout=10)
        data = res.json()
        arena_state["last_attacked_level"] = 0
        arena_state["last_patch_info"] = None
        add_event("ARENA_ORCHESTRATOR", "RESET", "Arena reset to vulnerable baseline for new evaluation round", data)
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/git/history")
async def git_history():
    try:
        res = subprocess.run(["git", "log", "-n", "6", "--pretty=format:%h|%s|%ar"], capture_output=True, text=True)
        commits = []
        for line in res.stdout.strip().split("\n"):
            if "|" in line:
                parts = line.split("|")
                commits.append({"hash": parts[0], "message": parts[1], "time": parts[2]})
        return {"commits": commits}
    except Exception as e:
        return {"commits": [], "error": str(e)}

@app.get("/api/git/diff")
async def git_diff():
    try:
        res = subprocess.run(["git", "diff", "HEAD~1", "HEAD", "active_target.py"], capture_output=True, text=True)
        return {
            "diff": res.stdout if res.stdout else "No uncommitted modifications.",
            "last_patch": arena_state.get("last_patch_info")
        }
    except Exception as e:
        return {"diff": f"Error: {str(e)}"}

@app.get("/api/telemetry/feed")
async def telemetry_feed():
    return {
        "status": "ok",
        "arena": "vibe-defender",
        "events": telemetry_events,
        "last_patch": arena_state.get("last_patch_info"),
        "count": len(telemetry_events)
    }
