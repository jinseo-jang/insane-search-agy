[English](README.md) | 한국어

<div align="center">

# insane-search for Antigravity

**Google Antigravity 2.0, IDE and CLI 전용 적응형 웹 스크래핑 & WAF 우회 플러그인**

<p>
  <img src="https://img.shields.io/badge/platform-Antigravity_2.0-4285F4?logo=googlecloud&style=flat-square" alt="Antigravity 2.0">
</p>

본 저장소는 오리지널 [fivetaku/insane-search](https://github.com/fivetaku/insane-search)를 Google Antigravity 2.0, IDE 및 CLI 환경에 맞게 재구축한 전용 파생 저장소(Antigravity Port)입니다.  
크롤링 엔진의 상세 알고리즘 및 21개 플랫폼 기본 사양은 [오리지널 저장소](https://github.com/fivetaku/insane-search)를 참고하세요.

</div>

---

## Antigravity 설치 가이드

### 1단계: Git 저장소 클론
```bash
git clone https://github.com/jinseo-jang/insane-search-agy.git
cd insane-search-agy
```

### 2단계: 스킬 디렉토리 복사

#### A. 전역(Global) 스킬 설치 (추천)
모든 Antigravity 2.0, IDE 및 CLI 세션에서 사용:
```bash
mkdir -p ~/.gemini/config/skills
cp -r skills/insane-search ~/.gemini/config/skills/
```

#### B. 프로젝트 로컬(Local) 스킬 설치
현재 프로젝트 워크스페이스 전용 설치:
```bash
mkdir -p .agents/skills
cp -r skills/insane-search .agents/skills/
```

---

## 사용법

자연어로 에이전트에게 요청하거나 슬래시 커맨드 및 CLI 모듈로 실행할 수 있습니다.

### 1. 자연어 프롬프트 요청 예시
- "쿠팡에서 아이폰 16 Pro 최저가 알려줘"
- "X(트위터)에서 Antigravity 관련 최신 트윗 요약해줘"
- "레딧 r/Python 인기 글 3개 가져와줘"
**자연어 프롬프트 트리거:** 트위터/X 못 열어, 레딧 안 읽혀, 유튜브 자막 뽑아줘, 깃헙 검색, 사이트 차단됨, 스레드 안 열려, 마스토돈, 미디엄, 서브스택, 스택오버플로우, 네이버 블로그, 디시인사이드, 에펨코리아, 요즘IT, 긱뉴스, 클리앙, 쿠팡, 링크드인, 당근마켓

### 2. 슬래시 커맨드 및 CLI 직접 실행
```bash
/insane-search <URL>

# CLI 직접 실행 (작업 디렉토리 이동):
cd skills/insane-search && python3 -m engine "<URL>"

# 또는 PYTHONPATH 지정 실행:
PYTHONPATH=skills/insane-search python3 -m engine "<URL>"
```

---

## 오리지널(Upstream)과의 주요 차이점

| 비교 항목 | 오리지널 상류 저장소 (`fivetaku/insane-search`) | Antigravity 전용 포트 (`insane-search-agy`) |
| :--- | :--- | :--- |
| **타겟 에이전트** | Claude Code CLI / 플러그인 생태계 | **Google Antigravity 2.0, IDE and CLI** |
| **스킬 설치 경로** | Claude 전용 레지스트리 (`claude plugin add`) | `~/.gemini/config/skills/` 및 `.agents/skills/` |
| **의존성 및 폴백 처리** | 사용자 사전 수동 설치 필요 | **크로스플랫폼 자가 감지 & Rule R6**: 엔진 내 macOS, Linux, Windows Node 감지 (예: `/opt/homebrew/bin/node`) 및 Rule R6 전수 시도 강제 규칙 적용, Patchright 자동 설치 (`npx patchright install chrome`) 지원 |
| **보안 경계** | 일반 텍스트 반환 | **Rule R8 보안 격리**: `[BEGIN UNTRUSTED WEB CONTENT]` 태그 적용 |

---

## 라이선스

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.  
Original work Copyright (c) 2026 fivetaku. Antigravity Port Copyright (c) 2026 Jinseo Jang.
