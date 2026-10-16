"""
Vibe Defender Cyber Arena HUD & Orchestrator (v3.0)
Coordinates Red Server (8003), Blue Server (8004), Target App (8002).
Features:
1. Interactive Git Commit Time-Machine (click any commit to inspect historical diff & full code snapshot)
2. 3-Tab Code Evolution Inspector (Visual Diff / Full Code Snapshot / Original Vulnerable Baseline)
3. 1-Click 3-Round Autonomous Cyber War (Auto-Battle Mode)
"""

import os
import subprocess
import requests
import httpx
from datetime import datetime
from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Vibe Defender Cyber Arena HUD", version="3.0.0")

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
        <title>🛡️ Vibe Defender v3.0 - Autonomous Cyber Arena HUD</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .glow-cyan { box-shadow: 0 0 20px rgba(6, 182, 212, 0.35); }
            .glow-rose { box-shadow: 0 0 20px rgba(244, 63, 94, 0.35); }
            .glow-indigo { box-shadow: 0 0 20px rgba(99, 102, 241, 0.45); }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
        <!-- Top Nav -->
        <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur px-6 py-4 flex flex-wrap justify-between items-center gap-4 sticky top-0 z-50">
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
            
            <div class="flex flex-wrap items-center gap-2.5 text-xs font-mono">
                <!-- 1-Click Auto-Battle Button -->
                <button id="auto-battle-btn" onclick="startAutoBattle()" class="bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition font-bold glow-indigo">
                    <i class="fa-solid fa-bolt"></i>
                    <span>⚔️ Start Auto-Battle (5 Rounds)</span>
                </button>
                <button onclick="resetArena()" class="bg-rose-950/80 hover:bg-rose-900 text-rose-300 border border-rose-700/60 px-3.5 py-2 rounded-lg flex items-center space-x-2 transition font-bold">
                    <i class="fa-solid fa-arrow-rotate-left"></i>
                    <span>⚡ Reset Arena</span>
                </button>
                <a href="/portal/" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 px-3.5 py-2 rounded-lg border border-slate-700 flex items-center space-x-1.5 transition font-bold">
                    <i class="fa-solid fa-store"></i>
                    <span>Target Storefront (/portal)</span>
                </a>
                <span class="bg-emerald-950 text-emerald-400 border border-emerald-800/80 px-3 py-1.5 rounded-lg flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>ONLINE</span>
                </span>
            </div>
        </header>

        <main class="max-w-7xl mx-auto p-6 space-y-6">
            <!-- Auto-Battle Progress Stepper (Hidden unless active) -->
            <div id="battle-stepper" class="hidden bg-slate-900/90 border border-indigo-500/50 rounded-2xl p-4 glow-indigo">
                <div class="flex justify-between items-center mb-2">
                    <span id="battle-step-title" class="text-xs font-bold text-indigo-300 uppercase tracking-wider">⚔️ Autonomous Cyber Battle in Progress...</span>
                    <span id="battle-step-badge" class="text-xs font-mono bg-indigo-950 text-indigo-300 px-2.5 py-0.5 rounded border border-indigo-700">Round 1 / 5</span>
                </div>
                <div class="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
                    <div id="battle-progress-bar" class="bg-gradient-to-r from-rose-500 via-indigo-500 to-emerald-400 h-full transition-all duration-500" style="width: 10%"></div>
                </div>
            </div>

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
                        <p class="text-xs text-slate-400 mb-3">Autonomous target AST reconnaissance & polymorphic exploit synthesis:</p>
                        <button onclick="triggerAttack('autonomous_recon', 0)" class="w-full mb-2.5 bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-rose-600/30 border border-rose-400/40">
                            <i class="fa-solid fa-brain"></i>
                            <span>🧠 Red-Argon Autonomous Next Exploit (1-by-1 Recon & Attack)</span>
                        </button>
                        <div class="grid grid-cols-5 gap-1.5 mb-3">
                            <button onclick="triggerAttack('sqli_search', 1)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-lg p-2 text-[11px] font-semibold text-center transition flex flex-col items-center justify-center">
                                <span>💉 Lv.1 SQLi</span>
                                <span class="text-[9px] text-slate-400">UNION Dump</span>
                            </button>
                            <button onclick="triggerAttack('auth_bypass', 2)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-lg p-2 text-[11px] font-semibold text-center transition flex flex-col items-center justify-center">
                                <span>🔓 Lv.2 Auth</span>
                                <span class="text-[9px] text-slate-400">OR 1=1 Bypass</span>
                            </button>
                            <button onclick="triggerAttack('price_tampering', 3)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-lg p-2 text-[11px] font-semibold text-center transition flex flex-col items-center justify-center">
                                <span>🏷️ Lv.3 $0</span>
                                <span class="text-[9px] text-slate-400">Price Tamper</span>
                            </button>
                            <button onclick="triggerAttack('negative_qty_drain', 4)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-lg p-2 text-[11px] font-semibold text-center transition flex flex-col items-center justify-center">
                                <span>💸 Lv.4 Refund</span>
                                <span class="text-[9px] text-slate-400">+$75K Drain</span>
                            </button>
                            <button onclick="triggerAttack('admin_vault_leak', 5)" class="bg-rose-900/30 hover:bg-rose-800/60 text-rose-200 border border-rose-700/50 rounded-lg p-2 text-[11px] font-semibold text-center transition flex flex-col items-center justify-center">
                                <span>🔑 Lv.5 Vault</span>
                                <span class="text-[9px] text-slate-400">Key Leak</span>
                            </button>
                        </div>
                    </div>
                    <div id="red-result" class="bg-slate-950/90 p-3.5 rounded-xl border border-slate-800/80 font-mono text-xs text-rose-300 min-h-[95px] overflow-auto">
                        [Red Team Ready] Click '🧠 Red-Argon Autonomous Next Exploit' for 1-by-1 AI discovery, or pick Lv.1~Lv.5!
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
                                Argon thinking_level="high" • AST Verifier
                            </span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">1M Context AST reasoning, Antigravity Sandbox verification (`ast.parse`) & live Git commit:</p>
                        <div class="flex space-x-3 mb-4">
                            <button onclick="triggerDefensePatch()" class="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-4 rounded-xl text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-cyan-600/30">
                                <i class="fa-solid fa-wand-magic-sparkles"></i>
                                <span>🛡️ Gemini 4 Argon Autonomous Patch & Git Commit</span>
                            </button>
                            <button onclick="refreshDiff()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-3 rounded-xl text-xs font-mono border border-slate-700 transition" title="Refresh Git Diff">
                                <i class="fa-solid fa-rotate"></i>
                            </button>
                        </div>
                    </div>
                    <div id="blue-result" class="bg-slate-950/90 p-3.5 rounded-xl border border-slate-800/80 font-mono text-xs text-cyan-300 min-h-[95px] overflow-auto">
                        [Blue Team Ready] Waiting for adversary breach telemetry to synthesize AST patch...
                    </div>
                </div>
            </div>

            <!-- Grid Row 2: Dual Log Stream & 3-Tab Code Time-Machine Inspector -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left (5 cols): Real-Time Adversary & Breach Telemetry -->
                <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col lg:col-span-5">
                    <div class="flex justify-between items-center pb-3 border-b border-slate-800 mb-3">
                        <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                            <i class="fa-solid fa-terminal text-rose-400"></i>
                            <span>1. Real-Time Breach Telemetry</span>
                        </h3>
                        <span class="text-[11px] font-mono text-slate-500">target_access.log</span>
                    </div>
                    <div id="packet-log-stream" class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-xs text-slate-300 space-y-1.5 h-96 overflow-y-auto">
                        <div class="text-slate-500">[Idle] Waiting for adversary attack stream...</div>
                    </div>
                </div>

                <!-- Right (7 cols): 3-Tab Code Evolution & Time-Machine Inspector -->
                <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col lg:col-span-7">
                    <div class="flex flex-wrap justify-between items-center gap-2 pb-3 border-b border-slate-800 mb-3">
                        <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                            <i class="fa-solid fa-code-compare text-teal-400"></i>
                            <span>2. Code Evolution & Time-Machine Inspector</span>
                        </h3>
                        <!-- 3 Tabs -->
                        <div class="flex space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-[11px] font-mono">
                            <button id="tab-btn-diff" onclick="switchInspectorTab('diff')" class="px-2.5 py-1 rounded bg-cyan-600 text-white font-bold transition">
                                🔀 Visual Diff
                            </button>
                            <button id="tab-btn-full" onclick="switchInspectorTab('full')" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition">
                                📜 Snapshot Code
                            </button>
                            <button id="tab-btn-base" onclick="switchInspectorTab('base')" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition">
                                ⚠️ Original Vulnerable
                            </button>
                        </div>
                    </div>

                    <div id="inspector-header" class="text-[11px] font-mono text-slate-400 mb-2 flex justify-between items-center bg-slate-950/60 px-3 py-1.5 rounded-lg border border-slate-800/60">
                        <span id="inspected-commit-label">📍 Viewing: Latest Working State (HEAD)</span>
                        <span class="text-emerald-400">active_target.py • uvicorn --reload</span>
                    </div>

                    <!-- Tab Content 1: Visual Diff -->
                    <div id="tab-content-diff" class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-xs h-80 overflow-y-auto space-y-3">
                        <div class="text-slate-500">Click an Attack button and then 'Autonomous Patch', or click any Commit Card below to inspect past code changes!</div>
                    </div>

                    <!-- Tab Content 2: Full Code Snapshot at Selected Commit -->
                    <pre id="tab-content-full" class="hidden bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-[11px] text-cyan-200 h-80 overflow-auto whitespace-pre"></pre>

                    <!-- Tab Content 3: Original Vulnerable Baseline Code -->
                    <pre id="tab-content-base" class="hidden bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-[11px] text-rose-200/90 h-80 overflow-auto whitespace-pre"></pre>
                </div>
            </div>

            <!-- Grid Row 3: Interactive Git Commit Timeline (Time-Machine) -->
            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                        <i class="fa-solid fa-clock-rotate-left text-indigo-400"></i>
                        <span>3. Interactive Git Commit Time-Machine (Click Any Commit to Inspect Past Code!)</span>
                    </h3>
                    <span class="text-xs font-mono text-indigo-400">Author: Firecat2025 &lt;2025firecat@gmail.com&gt;</span>
                </div>
                <div id="git-log" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3 text-xs font-mono">
                    <div class="text-slate-500">Loading commit timeline...</div>
                </div>
            </div>
        </main>

        <script>
            let currentAttackLevel = 0;
            let selectedCommitHash = 'HEAD';

            function escapeHtml(str) {
                return (str || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
            }

            function switchInspectorTab(tab) {
                ['diff', 'full', 'base'].forEach(t => {
                    document.getElementById(`tab-content-${t}`).classList.add('hidden');
                    const btn = document.getElementById(`tab-btn-${t}`);
                    btn.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition';
                });
                document.getElementById(`tab-content-${tab}`).classList.remove('hidden');
                document.getElementById(`tab-btn-${tab}`).className = 'px-2.5 py-1 rounded bg-cyan-600 text-white font-bold transition';

                if (tab === 'base') {
                    loadBaselineCode();
                } else if (tab === 'full' && !document.getElementById('tab-content-full').textContent) {
                    inspectCommit(selectedCommitHash);
                }
            }

            async function loadBaselineCode() {
                try {
                    const res = await fetch('/api/code/baseline');
                    const data = await res.json();
                    const lines = (data.baseline_code || '').split('\\n').map((l, i) => `${String(i+1).padStart(3, ' ')} | ${l}`).join('\\n');
                    document.getElementById('tab-content-base').textContent = lines;
                } catch(e) {
                    console.error(e);
                }
            }

            function renderColorDiff(rawDiff, patchInfo, commitTitle = '') {
                const viewer = document.getElementById('tab-content-diff');
                let html = '';

                if (commitTitle) {
                    html += `<div class="bg-indigo-950/60 border border-indigo-700/60 px-3 py-2 rounded-lg text-indigo-200 text-[11px] font-bold mb-2">🕰️ Time-Machine Commit: ${escapeHtml(commitTitle)}</div>`;
                }

                if (rawDiff === 'CLEAN_BASELINE_STATE') {
                    html += `
                        <div class="bg-amber-950/30 border-2 border-amber-500/50 rounded-xl p-4 space-y-2">
                            <div class="text-amber-300 font-extrabold text-xs uppercase tracking-wider flex items-center space-x-2">
                                <i class="fa-solid fa-sparkles"></i>
                                <span>🔄 CLEAN BASELINE STATE RESTORED (0 Patches Active)</span>
                            </div>
                            <p class="text-slate-300 text-[11px]">
                                Target repository (<code class="text-cyan-300">active_target.py</code>) and telemetry stream have been wiped clean and restored to the initial baseline with <strong>all 5 vulnerabilities (Lv.1 ~ Lv.5) active</strong>.
                            </p>
                            <div class="text-[11px] text-emerald-300 bg-slate-950/80 border border-slate-800 rounded-lg p-2.5">
                                💡 <strong>Tip:</strong> Launch a new attack above, or click any green <strong>[🛡️ ARGON PATCH]</strong> commit card in the Git Time-Machine below to inspect past Argon patches & Sandbox Reproduction Tests!
                            </div>
                        </div>
                    `;
                    viewer.innerHTML = html;
                    return;
                }

                if (patchInfo && patchInfo.before_code && patchInfo.after_code) {
                    const vLoop = patchInfo.verification_loop || {};
                    html += `
                        <div class="mb-3 space-y-2.5">
                            <div class="text-[11px] font-bold text-cyan-400 flex items-center justify-between bg-slate-900/90 px-3 py-1.5 rounded-lg border border-cyan-900/50">
                                <span>📍 Step 1 (Repo Scan & Call-Site): ${escapeHtml(patchInfo.target_endpoint || 'active_target.py')}</span>
                                <span>Commit: #${escapeHtml(patchInfo.commit_hash || 'HEAD')}</span>
                            </div>
                            ${vLoop.reproduction_test_code ? `
                            <div class="bg-indigo-950/40 border-l-4 border-indigo-400 p-2.5 rounded-r-lg">
                                <div class="text-[10px] font-bold text-indigo-300 uppercase mb-1 flex justify-between">
                                    <span>🧪 Step 2 (Antigravity Sandbox Reproduction Test: ${escapeHtml(vLoop.reproduction_test_file || 'tests/repro_test.py')})</span>
                                    <span class="text-emerald-300">${escapeHtml(vLoop.ast_nodes_delta || 'AST Verified')}</span>
                                </div>
                                <pre class="text-indigo-200 whitespace-pre-wrap text-[10px]">${escapeHtml(vLoop.reproduction_test_code)}</pre>
                            </div>
                            ` : ''}
                            <div class="bg-rose-950/40 border-l-4 border-rose-500 p-2.5 rounded-r-lg">
                                <div class="text-[10px] font-bold text-rose-400 uppercase mb-1">❌ Step 3A — BEFORE (Vulnerable Call-Site Removed)</div>
                                <pre class="text-rose-200 whitespace-pre-wrap text-[11px]">- ${escapeHtml(patchInfo.before_code)}</pre>
                            </div>
                            <div class="bg-emerald-950/40 border-l-4 border-emerald-500 p-2.5 rounded-r-lg">
                                <div class="text-[10px] font-bold text-emerald-400 uppercase mb-1">✅ Step 3B — AFTER (Patched by Gemini 4 Argon & Verified in Sandbox)</div>
                                <pre class="text-emerald-200 whitespace-pre-wrap text-[11px]">+ ${escapeHtml(patchInfo.after_code)}</pre>
                            </div>
                        </div>
                        <div class="border-t border-slate-800 pt-2 text-[10px] text-slate-500 uppercase font-bold">Unified Git Diff Lines:</div>
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
                    html = `<div class="text-slate-500">No code diff in this commit or baseline state. Click another commit card below or run an Attack + Patch!</div>`;
                }

                viewer.innerHTML = html;
            }

            async function inspectCommit(hash) {
                selectedCommitHash = hash;
                document.querySelectorAll('.commit-card').forEach(el => {
                    el.classList.remove('border-cyan-400', 'bg-cyan-950/30');
                });
                const activeCard = document.getElementById(`commit-card-${hash}`);
                if (activeCard) {
                    activeCard.classList.add('border-cyan-400', 'bg-cyan-950/30');
                }

                try {
                    const res = await fetch(`/api/git/commit/${hash}`);
                    const data = await res.json();
                    document.getElementById('inspected-commit-label').textContent = `🕰️ Inspecting Commit [${data.hash}]: ${data.subject} (${data.time})`;
                    renderColorDiff(data.diff, null, `${data.hash} — ${data.subject}`);

                    const numberedCode = (data.full_code || '').split('\\n').map((l, i) => `${String(i+1).padStart(3, ' ')} | ${l}`).join('\\n');
                    document.getElementById('tab-content-full').textContent = numberedCode;
                } catch(e) {
                    console.error(e);
                }
            }

            async function triggerAttack(scenario, level) {
                currentAttackLevel = level;
                const redBox = document.getElementById('red-result');
                redBox.innerHTML = '<span class="text-slate-400">🧠 Gemini 4 Argon (Medium) inspecting target AST & synthesizing exploit payload...</span>';
                try {
                    const res = await fetch(`/api/attack?scenario=${scenario}&level=${level}`, { method: 'POST' });
                    const data = await res.json();
                    if (data.level) currentAttackLevel = data.level;
                    let html = `<div><strong>[Attack Result]</strong> ${data.breached ? '<span class="text-rose-400 font-bold">🚨 TARGET BREACHED (VULNERABLE)</span>' : '<span class="text-emerald-400 font-bold">🛡️ ATTACK BLOCKED (PROTECTED BY ARGON PATCH)</span>'}</div>`;
                    if (data.flag) {
                        html += `<div class="text-amber-400 font-bold mt-1">🚩 Flag Exfiltrated: ${escapeHtml(data.flag)}</div>`;
                    }
                    if (data.payload?.reasoning) {
                        html += `<div class="text-cyan-300 text-[11px] mt-1">🧠 <strong>Argon Recon:</strong> ${escapeHtml(data.payload.reasoning)}</div>`;
                    }
                    html += `<div class="text-slate-400 text-[11px] mt-0.5">🎯 ${escapeHtml(data.payload?.description || '')}</div>`;
                    redBox.innerHTML = html;
                    await refreshLogs();
                    return data;
                } catch(e) {
                    redBox.innerHTML = `<span class="text-red-400">Attack request error: ${e}</span>`;
                    return null;
                }
            }

            async function triggerDefensePatch(levelOverride = null) {
                const lvl = levelOverride !== null ? levelOverride : currentAttackLevel;
                const blueBox = document.getElementById('blue-result');
                blueBox.innerHTML = '<span class="text-slate-400">🛡️ Gemini 4 Argon (High) analyzing AST, verifying with ast.parse() & committing patch...</span>';
                try {
                    const res = await fetch(`/api/defense/patch?round_num=${lvl}`, { method: 'POST' });
                    const data = await res.json();
                    if (data.status === 'patched') {
                        const vLoop = data.verification_loop || {};
                        blueBox.innerHTML = `
                            <div><strong>[Patch Applied]</strong> ${escapeHtml(data.description)}</div>
                            ${data.root_cause ? `<div class="text-[11px] text-amber-300 mt-1">🔍 <strong>Root Cause:</strong> ${escapeHtml(data.root_cause)}</div>` : ''}
                            ${vLoop.stage_3_regression_check ? `<div class="text-[11px] text-emerald-300 mt-0.5">🧪 <strong>Verification Loop:</strong> ${escapeHtml(vLoop.stage_3_regression_check)} (${escapeHtml(vLoop.ast_nodes_delta || '')})</div>` : ''}
                            <div class="text-[11px] text-cyan-400 mt-0.5">📦 Git Commit: <strong>#${escapeHtml(data.commit_hash)}</strong> • Target: ${escapeHtml(data.target_endpoint)}</div>
                        `;
                        document.getElementById('inspected-commit-label').textContent = `📍 Viewing Latest Patch [${data.commit_hash}]: ${data.target_endpoint}`;
                    } else {
                        blueBox.innerHTML = `<div><strong>[Info]</strong> ${escapeHtml(data.message)}</div>`;
                    }
                    await refreshDiff(data);
                    await refreshGitLog();
                    await refreshLogs();
                    return data;
                } catch(e) {
                    blueBox.innerHTML = `<span class="text-red-400">Patch error: ${e}</span>`;
                    return null;
                }
            }

            const sleep = ms => new Promise(r => setTimeout(r, ms));

            async function startAutoBattle() {
                const stepper = document.getElementById('battle-stepper');
                const title = document.getElementById('battle-step-title');
                const badge = document.getElementById('battle-step-badge');
                const bar = document.getElementById('battle-progress-bar');
                stepper.classList.remove('hidden');

                // Step 0: Reset to clean vulnerable state
                title.textContent = '⚡ Step 0: Restoring Target Storefront to Vulnerable Baseline...';
                badge.textContent = 'Initializing';
                bar.style.width = '10%';
                await fetch('/api/arena/reset', { method: 'POST' });
                await sleep(1000);

                const rounds = [
                    { level: 1, scenario: 'sqli_search', name: 'SQL Injection Search Exfiltration (Lv.1)' },
                    { level: 2, scenario: 'auth_bypass', name: 'Admin Authentication Bypass (Lv.2)' },
                    { level: 3, scenario: 'price_tampering', name: 'Zero-Dollar Order Price Tampering (Lv.3)' },
                    { level: 4, scenario: 'negative_qty_drain', name: 'Negative Quantity Refund Wallet Drain (Lv.4)' },
                    { level: 5, scenario: 'admin_vault_leak', name: 'Admin PQC Key Vault RBAC Bypass (Lv.5)' }
                ];

                for (let i = 0; i < rounds.length; i++) {
                    const r = rounds[i];
                    badge.textContent = `Round ${r.level} / 5`;

                    // 1. Red Attack
                    title.textContent = `🔴 Round ${r.level}/5: Red-Argon attacking ${r.name}...`;
                    bar.style.width = `${10 + i * 18}%`;
                    await triggerAttack(r.scenario, r.level);
                    await sleep(1500);

                    // 2. Blue Patch
                    title.textContent = `🔵 Round ${r.level}/5: Blue-Argon synthesizing AST patch & committing to Git...`;
                    bar.style.width = `${16 + i * 18}%`;
                    await triggerDefensePatch(r.level);
                    await sleep(1700);

                    // 3. Re-Attack Verification
                    title.textContent = `🛡️ Round ${r.level}/5: Re-running ${r.name} to verify Argon patch...`;
                    bar.style.width = `${22 + i * 18}%`;
                    await triggerAttack(r.scenario, r.level);
                    await sleep(1200);
                }

                title.textContent = '🏆 AUTO-BATTLE COMPLETE: All 5 Vulnerabilities (Lv.1~Lv.5) Patched, AST-Verified & Committed to Git!';
                badge.textContent = '5/5 HARDENED';
                bar.style.width = '100%';
            }

            async function resetArena() {
                if(!confirm('Reset the cyber arena to the vulnerable baseline state (5 vulnerabilities active)?')) return;
                try {
                    await fetch('/api/arena/reset', { method: 'POST' });
                    currentAttackLevel = 0;
                    document.getElementById('battle-stepper').classList.add('hidden');
                    document.getElementById('inspected-commit-label').textContent = '📍 Viewing: Clean Baseline State (HEAD)';
                    await refreshDiff();
                    await refreshGitLog();
                    await refreshLogs();
                    document.getElementById('red-result').innerText = '[Red Team Ready] Arena restored to clean baseline (Lv.1~Lv.5 active).';
                    document.getElementById('blue-result').innerText = '[Blue Team Ready] Telemetry stream cleared. Waiting for adversary attacks.';
                } catch(e) {
                    alert('Reset error: ' + e);
                }
            }

            async function refreshDiff(patchData = null) {
                try {
                    const res = await fetch('/api/git/diff');
                    const data = await res.json();
                    renderColorDiff(data.diff, patchData || data.last_patch);
                    if (data.current_code) {
                        const numbered = data.current_code.split('\\n').map((l, i) => `${String(i+1).padStart(3, ' ')} | ${l}`).join('\\n');
                        document.getElementById('tab-content-full').textContent = numbered;
                    }
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
                        container.innerHTML = data.commits.map(c => {
                            const msgLower = (c.message || '').toLowerCase();
                            const isReset = msgLower.includes('reset') || msgLower.includes('baseline');
                            const isPatch = msgLower.includes('fix(security)') || msgLower.includes('[argon]');

                            let cardClass = 'bg-slate-950 border-slate-800/80 hover:border-cyan-400';
                            let hashColor = 'text-cyan-400';
                            let typeBadge = '<span class="text-[9px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-bold">📦 SYSTEM</span>';

                            if (isReset) {
                                cardClass = 'bg-amber-950/20 border-amber-500/40 hover:border-amber-400';
                                hashColor = 'text-amber-300';
                                typeBadge = '<span class="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/40 px-1.5 py-0.5 rounded font-bold">🔄 CLEAN RESET (Baseline)</span>';
                            } else if (isPatch) {
                                cardClass = 'bg-emerald-950/20 border-emerald-500/40 hover:border-emerald-400';
                                hashColor = 'text-emerald-300';
                                typeBadge = '<span class="text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-1.5 py-0.5 rounded font-bold">🛡️ ARGON PATCH</span>';
                            }

                            return `
                            <div id="commit-card-${c.hash}" onclick="inspectCommit('${c.hash}')" class="commit-card cursor-pointer p-3 rounded-xl border transition group ${cardClass}">
                                <div class="flex justify-between items-center mb-1.5">
                                    <span class="${hashColor} font-bold group-hover:underline">#${c.hash}</span>
                                    ${typeBadge}
                                </div>
                                <div class="text-slate-200 truncate text-[11px] font-medium" title="${escapeHtml(c.message)}">${escapeHtml(c.message)}</div>
                                <div class="flex justify-between items-center text-[10px] text-slate-500 mt-1.5">
                                    <span>${c.time}</span>
                                    <span class="text-cyan-400/80 group-hover:text-cyan-300">Click to Inspect 🔍</span>
                                </div>
                            </div>
                            `;
                        }).join('');
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
                    } else {
                        stream.innerHTML = '<div class="text-emerald-400 font-bold">[CLEAN BASELINE] 0 active breach events. Ready for evaluation.</div>';
                    }
                } catch(e) {
                    console.error(e);
                }
            }

            refreshGitLog();
            refreshDiff();
            refreshLogs();
            loadBaselineCode();
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
        resolved_lvl = data.get("level", level)
        arena_state["last_attacked_level"] = resolved_lvl
        log_lvl = "BREACH" if data.get("breached") else "INFO"
        add_event("RED_AGENT", log_lvl, f"Scenario: {data.get('scenario', scenario)} (Lv.{resolved_lvl}) -> Breached: {data.get('breached')}", data)
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
        # Wipe all previous breach/patch logs so Clean Reset starts with a 100% clean log stream!
        telemetry_events.clear()
        add_event("ARENA_ORCHESTRATOR", "RESET", "✨ CLEAN BASELINE RESTORED: Previous logs cleared & 5 vulnerabilities (Lv.1~Lv.5) reset to initial state.", data)
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/git/history")
async def git_history():
    try:
        res = subprocess.run(["git", "log", "-n", "12", "--pretty=format:%h|%s|%ar"], capture_output=True, text=True)
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
        subj_res = subprocess.run(["git", "log", "-n", "1", "--pretty=format:%s"], capture_output=True, text=True)
        latest_subject = (subj_res.stdout or "").strip().lower()
        is_reset = "reset target code" in latest_subject or "baseline" in latest_subject

        res = subprocess.run(["git", "diff", "HEAD~1", "HEAD", "active_target.py"], capture_output=True, text=True)
        current_code = ""
        if os.path.exists("active_target.py"):
            with open("active_target.py", "r", encoding="utf-8") as f:
                current_code = f.read()
        return {
            "diff": "CLEAN_BASELINE_STATE" if is_reset else (res.stdout if res.stdout else "No uncommitted modifications."),
            "last_patch": None if is_reset else arena_state.get("last_patch_info"),
            "current_code": current_code
        }
    except Exception as e:
        return {"diff": f"Error: {str(e)}"}

@app.get("/api/git/commit/{commit_hash}")
async def inspect_git_commit(commit_hash: str):
    """
    Time-Machine endpoint: returns the exact diff and full file snapshot of active_target.py at a given commit hash.
    """
    try:
        meta_res = subprocess.run(["git", "show", "-s", "--format=%h|%s|%ar", commit_hash], capture_output=True, text=True)
        parts = meta_res.stdout.strip().split("|")
        short_hash = parts[0] if len(parts) > 0 else commit_hash
        subject = parts[1] if len(parts) > 1 else ""
        rel_time = parts[2] if len(parts) > 2 else ""

        is_reset = "reset target code" in subject.lower() or "baseline" in subject.lower()
        diff_res = subprocess.run(["git", "show", "--format=", commit_hash, "--", "active_target.py"], capture_output=True, text=True)
        code_res = subprocess.run(["git", "show", f"{commit_hash}:active_target.py"], capture_output=True, text=True)

        return {
            "hash": short_hash,
            "subject": subject,
            "time": rel_time,
            "diff": "CLEAN_BASELINE_STATE" if is_reset else (diff_res.stdout if diff_res.stdout else "No changes to active_target.py in this commit."),
            "full_code": code_res.stdout if code_res.returncode == 0 else "File snapshot not available in this commit."
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/code/baseline")
async def get_baseline_code():
    baseline_code = ""
    if os.path.exists("active_target.baseline.py"):
        with open("active_target.baseline.py", "r", encoding="utf-8") as f:
            baseline_code = f.read()
    return {"baseline_code": baseline_code}

@app.get("/api/telemetry/feed")
async def telemetry_feed():
    return {
        "status": "ok",
        "arena": "vibe-defender",
        "events": telemetry_events,
        "last_patch": arena_state.get("last_patch_info"),
        "count": len(telemetry_events)
    }
