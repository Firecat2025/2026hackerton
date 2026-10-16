# 🛡️ Vibe Defender: AI Autonomous Cyber Arena & Live Code Evolution

> **2026 Hackathon Project**: AI 기반 자율 레드팀(공격)과 블루팀(방어)이 실시간으로 코드를 수정·검증·배포하는 자율 사이버 공방 및 관제 플랫폼

---

## 📌 주요 특징
1. **실시간 자율 방어 (Live Self-Healing)**: 타겟 애플리케이션 취약점 탐지 시 블루팀 AI 에이전트가 코드를 직접 수정하고 `git commit` 및 hot-reload(`uvicorn --reload`) 무중단 적용.
2. **현실적인 공격 시뮬레이션 (Red Team Orchestration)**: SQL Injection, IDOR, Prompt Injection 등 다단계 공격 시나리오 자동 실행.
3. **심사위원용 실시간 관제 HUD**: 공격 로그, 패치 전/후 코드 diff, 시스템 상태를 실시간 웹 대시보드(Port 8080)로 시각화.
4. **GCP 무위험 보안 아키텍처**: 인바운드 방화벽 개방 없이 **Cloudflare Tunnel**로 100% 안전한 공인 HTTPS 도메인 연결.

---

## 🏗️ 아키텍처 구성

- **방어 대상 서버 (Target / Blue)**: `127.0.0.1:8002` (`uvicorn active_target:app --reload`)
- **공격 및 메인 관제 서버 (HUD & Red)**: `127.0.0.1:8080` (`python3 server.py`)
- **보안 공인 터널**: `cloudflared tunnel --url http://localhost:8080` (HTTPS 발급)

---

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. GCE VM 배포 및 동기화
```bash
# 로컬 코드를 GCE VM으로 전송
gcloud compute scp --recurse . vibe-defender-vm:~/vibe-defender --zone=asia-northeast3-a
```

### 3. GCE 내부 실행
```bash
# GCE VM 접속 후
cd ~/vibe-defender
./scripts/run_all.sh
```
