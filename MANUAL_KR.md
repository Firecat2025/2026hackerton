# 🛡️ Vibe Defender v4.0: 한국어 공식 운영 및 심사 대응 매뉴얼 (MANUAL_KR)

> **대회명**: Google DeepMind AI Hackathon 2026  
> **트랙**: Track 4: Open innovation — autonomous agents and developer tools  
> **공식 GitHub 레포지토리**: https://github.com/Firecat2025/2026hackerton  
> **실시간 GitHub 커밋 확인**: https://github.com/Firecat2025/2026hackerton/commits/main

---

## 📌 목차 (Table of Contents)

1. [핵심 요약 & 라이브 링크](#1-핵심-요약--라이브-링크)
2. [GCP 계정과 GitHub 계정의 역할 구분](#2-gcp-계정과-github-계정의-역할-구분)
3. [GCE 서버 내부 동작 및 깃허브 실시간 푸시 메커니즘](#3-gce-서버-내부-동작-및-깃허브-실시간-푸시-메커니즘)
4. [5단계 실전 취약점 라운드 구조](#4-5단계-실전-취약점-라운드-구조)
5. [심사위원 1분 라이브 시연 스크립트](#5-심사위원-1분-라이브-시연-스크립트)
6. [심사위원 예상 질문 및 모범 답변 (Q&A Defense)](#6-심사위원-예상-질문-및-모범-답변-qa-defense)

---

## 1. 핵심 요약 & 라이브 링크

Vibe Defender v4.0은 구글 딥마인드 해커톤 Track 4의 핵심 도전 과제인 **"저장소 취약점 탐지 ➔ Antigravity 샌드박스 재현 테스트 작성 ➔ Gemini 4 Argon 기반 코드 패치 ➔ 비주얼 Diff 워크스루"**를 100% 실구현한 자율 사이버 보안 에이전트 시스템입니다.

- **⚔️ Cyber Arena HUD (운영 콘솔)**:  
  👉 **https://updates-useful-identical-festivals.trycloudflare.com/**
- **🛒 Target Storefront (실시간 변조/치유 쇼핑몰)**:  
  👉 **https://updates-useful-identical-festivals.trycloudflare.com/portal/**
- **🐙 GitHub 공식 저장소**:  
  👉 **https://github.com/Firecat2025/2026hackerton**
- **📜 Live GitHub Commits (실시간 커밋 스트림)**:  
  👉 **https://github.com/Firecat2025/2026hackerton/commits/main**

---

## 2. GCP 계정과 GitHub 계정의 역할 구분

두 계정이 어떤 역할을 하는지 심사위원에게 정확하게 설명할 수 있습니다:

| 계정 | 소속 / 플랫폼 | 실제 수행 역할 |
| :--- | :--- | :--- |
| **`devstar2630@gcplab.me`** | **Google Cloud Platform (GCP)** | **클라우드 인프라 소유자 (VM Host)**<br>GCE 가상머신(`vibe-defender-vm`)과 네트워크, 프로젝트(`h2gdm-hack26icn-2630`)를 실행하는 계정입니다. Git 코드 작성과는 무관합니다. |
| **`2025firecat@gmail.com`<br>(ID: Firecat2025)** | **GitHub** | **소스코드의 공식 작성자 (Git Author & Committer)**<br>GCE 서버 내부의 Git 인증 설정(`~/.git-credentials`)에 등록되어 있어, Gemini 4 Argon이 생성한 모든 보안 패치 커밋이 GitHub에 `Firecat2025` 명의로 실시간 기록됩니다. |

---

## 3. GCE 서버 내부 동작 및 깃허브 실시간 푸시 메커니즘

버튼을 누를 때 브라우저 흉내가 아닌, **GCE 리눅스 서버 내부에서 실제로 일어나는 엔지니어링 과정**입니다:

```
[사용자 HUD 클릭]
       │
       ▼
[Cloudflare Zero-Trust Tunnel]
       │
       ▼
[GCE VM: agents/blue_server.py (Port 8004)]
       │
       ├─► (1) Gemini 4 Argon 심층 추론 (thinking_level="high")
       │       `client.interactions.create` 호출로 안전한 AST 코드 생성
       │
       ├─► (2) Antigravity Sandbox 재현 테스트 자동 생성 & 검증
       │       `tests/repro_test_lv*.py` 실행 및 `ast.parse()` 문법 검사
       │
       ├─► (3) 실제 리눅스 디스크 파일 쓰기
       │       `/home/PC/vibe-defender/active_target.py` 덮어쓰기
       │
       ├─► (4) GCE 로컬 Git 커밋 & 0.3초 무중단 핫리로드
       │       `git add active_target.py` && `git commit -m "fix(security)..."`
       │       `uvicorn --reload`가 커널 이벤트를 감지하여 0.3초 만에 새 코드 적용
       │
       └─► (5) 🚀 GitHub 원격 저장소 비동기 실시간 푸시 (Background Push)
               `subprocess.Popen(["git", "push", "origin", "HEAD:main", "--force"])`
               UI 응답은 0.05초 만에 완료되고, 1.5초 내에 github.com에 커밋이 나타남!
```

---

## 4. 5단계 실전 취약점 라운드 구조

| 레벨 | 취약점 종류 & 엔드포인트 | 공격 방식 (Red Argon) | Argon 패치 방식 (Blue Argon) |
| :---: | :--- | :--- | :--- |
| **Lv.1** | **검색창 SQL Injection**<br>`GET /api/search` | UNION 쿼리로 관리자 계정 정보 및 시크릿 플래그 유출 | raw f-string 문자열 결합을 파라미터 바인딩(`?`)으로 리팩토링 |
| **Lv.2** | **관리자 로그인 인증 우회**<br>`POST /api/login` | `admin' OR '1'='1'--` 항진식으로 패스워드 없이 root 권한 탈취 | `WHERE username = ? AND password = ?` 안전 바인딩 적용 |
| **Lv.3** | **0원 가격 변조 결제 탈취**<br>`POST /api/order` | 클라이언트가 $1,500 상품을 `unit_price: 0`으로 조작해 0원 결제 | 서버에서 DB의 실제 `products` 카탈로그 가격과 오차 검증 가드 추가 |
| **Lv.4** | **음수 수량 환불 지갑 탈취**<br>`POST /api/refund` | `quantity: -50` 음수 곱셈 반전으로 지갑에 `+$75,000` 무단 충전 | 엄격한 양수 수량 범위 가드(`0 < req.quantity <= 10`) 삽입 |
| **Lv.5** | **PQC 암호 마스터 키 유출**<br>`GET /api/admin/export` | 미인가 엔드포인트 무단 호출로 양자내성 암호 마스터 키 유출 | 상수 시간 `hmac.compare_digest` 기반 `X-Admin-Token` 헤더 RBAC 가드 생성 |

---

## 5. 심사위원 1분 라이브 시연 스크립트

### 1단계: 듀얼 창 준비
1. 좌측 화면: **[Cyber Arena HUD](https://updates-useful-identical-festivals.trycloudflare.com/)**
2. 우측 화면: **[Target Storefront](https://updates-useful-identical-festivals.trycloudflare.com/portal/)**
3. 보조 탭: **[GitHub Commits 스트림](https://github.com/Firecat2025/2026hackerton/commits/main)**

### 2단계: 클린 초기화 확인
- HUD 우측 상단 **`[⚡ Reset Arena]`** 클릭.
- **포인트 어필**: 텔레메트리 로그가 0건으로 비워지고, Visual Diff 탭에 Clean Baseline 카드가 표시되며, 쇼핑몰에 `5 VULNERABLE` 배지가 뜹니다.

### 3단계: 5라운드 자동 배틀 실행
- **`[⚔️ Start Auto-Battle (5 Rounds)]`** 버튼 클릭!
- **포인트 어필**:
  - Red Argon이 침투하여 쇼핑몰 가격이 **`$0 HACKED!`**로 변조되고 계정이 탈취되는 모습.
  - Blue Argon이 취약점을 진단하고 **Antigravity Sandbox 재현 테스트**를 통과시키는 로그.
  - 0.3초 만에 핫리로드되면서 쇼핑몰 가격이 **`$1,500`으로 자동 복구(Self-Healing)**되는 장면.
  - 상단 배지가 **`🛡️ 5 / 5 PATCHED`**로 전환되는 모습.

### 4단계: 깃허브 실시간 동기화 증명
- GitHub 커밋 페이지를 새로고침하여 방금 생성된 커밋 해시가 깃허브 웹사이트에 그대로 나타난 것을 확인시켜 줍니다.
- HUD의 **`🔀 Visual Diff`** 탭에서 3단계 워크스루(호출부 진단 ➔ 재현 테스트 코드 ➔ BEFORE/AFTER 비교)를 보여줍니다.

---

## 6. 심사위원 예상 질문 및 모범 답변 (Q&A Defense)

### Q1. "단순한 정규식 치환이나 화면상의 시뮬레이션 아닌가요?"
> **답변**: "아닙니다. 100% 구글 클라우드 GCE 리눅스 가상머신 내부에서 실행되는 실제 시스템입니다. 버튼을 누르면 Gemini 4 Argon이 `client.interactions.create` API를 통해 AST 수준의 파이썬 코드를 생성하고, 파이썬 프로세스가 리눅스 디스크에 있는 `active_target.py`를 직접 덮어쓴 뒤 `git commit`과 `git push`를 실행합니다. GitHub 저장소의 실시간 커밋 로그나 GCE 터미널의 `git diff`를 통해 확인하실 수 있습니다."

### Q2. "패치된 코드가 안전한지, 혹은 서비스가 깨지지 않는지 어떻게 보장하나요?"
> **답변**: "Blue Argon은 패치 코드를 적용하기 전에 `_execute_sandbox_verification_loop`를 통해 두 가지 검증을 거칩니다:
> 1. 취약점을 증명하는 **재현 테스트(`tests/repro_test_lv*.py`)**를 Antigravity 샌드박스에서 선행 생성 및 실행합니다.
> 2. `ast.parse()`를 통해 패치 코드의 파이썬 구문 트리가 100% 유효한지 검사하여 구문 오류(SyntaxError)를 사전에 차단합니다.
> 패치 적용 후에는 uvicorn이 0.3초 만에 무중단 핫리로드(Hot-reload)합니다."

### Q3. "왜 Gemini 4 Argon 모델을 사용했나요?"
> **답변**: "보안 패치는 단순 코드 완성이 아니라, 전체 애플리케이션의 AST 구조와 데이터베이스 스키마, 그리고 수 메가바이트의 서버 엑세스 로그를 동시에 이해해야 하는 고난도 추론 작업입니다. Gemini 4 Argon의 1M 통합 컨텍스트 윈도우와 `thinking_level="high"` 심층 추론 기능 덕분에 코드 잘림 없이 완벽한 리팩토링 코드를 한 번에 합성할 수 있었습니다."

---
*Vibe Defender v4.0 — Google DeepMind AI Hackathon 2026*
