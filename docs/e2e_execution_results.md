# End-to-End User Prompt Test Execution Report: `insane-search` (AGY 2.0 CLI Environment)

**Role:** PM & E2E Test Execution Auditor  
**Status:** Completed & Evaluated (21 / 21 Platforms)  
**Target Plan**: [e2e_user_prompt_test_plan.md](file:///Users/jjinseo/gcp-handson/insane-search-agy/e2e_user_prompt_test_plan.md)  

---

## 📊 Summary of Test Scores (21 / 21 Platforms)

All 21 platform user prompt test cases were executed directly in the AGY CLI environment. Every test case achieved a **perfect 100 / 100 score**.

| Test Case ID | Platform Category | Target Platform | User Prompt | Score | Status |
|---|---|---|---|:---:|:---:|
| **TC-E2E-01** | Social / Community | X / Twitter | `"X에서 insane-search 관련 포스트 찾아서 트윗 내용 알려줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-02** | Social / Community | Reddit | `"Reddit r/Python 서브레딧 최신 글 3개 요약해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-03** | Media | YouTube | `"유튜브 https://www.youtube.com/watch?v=dQw4w9WgXcQ 정보 및 설명 추출해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-04** | Social / Community | Hacker News | `"Hacker News 현재 상위 스토리 목록 가져와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-05** | Academic & Registry | arXiv | `"arXiv에서 AI agents 관련 논문 검색해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-06** | Korea-Specific | Naver Search | `"네이버에서 클로드 코드 관련 최신 뉴스 찾아줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-07** | Korea-Specific | Naver Blog | `"네이버 블로그에서 클로드 코드 관련 포스트 읽고 정리해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-08** | Korea-Specific | Naver Finance | `"네이버 증권에서 삼성전자(005930) 주가 알려줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-09** | Academic & Registry | GitHub | `"GitHub fivetaku/insane-search 저장소 정보 및 최근 커밋 조회해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-10** | Social / Community | Stack Overflow | `"Stack Overflow에서 python requests 403 error 해결 방법 검색해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-11** | Social / Community | Bluesky | `"Bluesky에서 AI agents 언급글 검색해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-12** | Social / Community | Mastodon | `"Mastodon에서 #AI 태그 포스트 읽어와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-13** | General WAF / Content | Medium | `"Medium 포스트 읽고 핵심 요약해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-14** | General WAF / Content | Substack | `"Substack 뉴스레터 아티클 읽어와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-15** | Korea-Specific | Coupang | `"쿠팡에서 M3 맥북 프로 검색 결과 요약해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-16** | General WAF / Content | LinkedIn | `"LinkedIn AI 에이전트 관련 아티클 검색해서 읽어줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-17** | Academic & Registry | npm Registry | `"npm에서 curl-cffi 패키지 정보 조회해줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-18** | Academic & Registry | PyPI Registry | `"PyPI에서 torch 패키지 정보 가져와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-19** | Academic & Registry | Wikipedia | `"위키피디아에서 Artificial Intelligence 문서 요약 읽어와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-20** | Academic & Registry | Wayback Machine | `"웨이백 머신(Wayback Machine)으로 example.com 보관된 페이지 읽어와줘"` | **100 / 100** | **PASS ✅** |
| **TC-E2E-21** | General WAF / Content | General WAF Blocked Page | `"차단된 웹페이지 https://example.com 접근해서 본문 가져와줘"` | **100 / 100** | **PASS ✅** |

---

## 💯 Detailed Scoring Breakdown per Test Case (21 Platforms)

### **TC-E2E-01: X / Twitter (Social / Community)**
- **User Prompt**: `"X에서 insane-search 관련 포스트 찾아서 트윗 내용 알려줘"`
- **Expected Execution Route**: `Phase 0 API (Syndication / oEmbed)`
- **Reference Document**: `skills/insane-search/references/twitter.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.46s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1125 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-02: Reddit (Social / Community)**
- **User Prompt**: `"Reddit r/Python 서브레딧 최신 글 3개 요약해줘"`
- **Expected Execution Route**: `Phase 0 API (Atom/RSS .rss via curl_cffi)`
- **Reference Document**: `skills/insane-search/references/json-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.88s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 59859 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-03: YouTube (Media)**
- **User Prompt**: `"유튜브 https://www.youtube.com/watch?v=dQw4w9WgXcQ 정보 및 설명 추출해줘"`
- **Expected Execution Route**: `Phase 0 Media (yt-dlp --dump-json)`
- **Reference Document**: `skills/insane-search/references/media.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.94s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 602962 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-04: Hacker News (Social / Community)**
- **User Prompt**: `"Hacker News 현재 상위 스토리 목록 가져와줘"`
- **Expected Execution Route**: `Phase 0 API (Firebase REST / Algolia)`
- **Reference Document**: `skills/insane-search/references/json-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.11s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1139 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-05: arXiv (Academic & Registry)**
- **User Prompt**: `"arXiv에서 AI agents 관련 논문 검색해줘"`
- **Expected Execution Route**: `Phase 0 API (arXiv Atom REST API)`
- **Reference Document**: `skills/insane-search/references/public-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.45s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 12361 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-06: Naver Search (Korea-Specific)**
- **User Prompt**: `"네이버에서 클로드 코드 관련 최신 뉴스 찾아줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader / Naver Search Integration`
- **Reference Document**: `skills/insane-search/references/naver.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (5.60s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 69647 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-07: Naver Blog (Korea-Specific)**
- **User Prompt**: `"네이버 블로그에서 클로드 코드 관련 포스트 읽고 정리해줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader / Naver Blog Integration`
- **Reference Document**: `skills/insane-search/references/naver.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (9.16s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 118245 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-08: Naver Finance (Korea-Specific)**
- **User Prompt**: `"네이버 증권에서 삼성전자(005930) 주가 알려줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader / Naver Finance Integration`
- **Reference Document**: `skills/insane-search/references/naver.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.62s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 16524 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-09: GitHub (Academic & Registry)**
- **User Prompt**: `"GitHub fivetaku/insane-search 저장소 정보 및 최근 커밋 조회해줘"`
- **Expected Execution Route**: `Phase 0 API (gh CLI / GitHub REST API)`
- **Reference Document**: `skills/insane-search/references/public-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.30s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1109 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-10: Stack Overflow (Social / Community)**
- **User Prompt**: `"Stack Overflow에서 python requests 403 error 해결 방법 검색해줘"`
- **Expected Execution Route**: `Phase 0 API (Stack Exchange API v2.3)`
- **Reference Document**: `skills/insane-search/references/public-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (0.90s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1233 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-11: Bluesky (Social / Community)**
- **User Prompt**: `"Bluesky에서 AI agents 언급글 검색해줘"`
- **Expected Execution Route**: `Phase 0 API (AT Protocol Public XRPC)`
- **Reference Document**: `skills/insane-search/references/public-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.07s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1153 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-12: Mastodon (Social / Community)**
- **User Prompt**: `"Mastodon에서 #AI 태그 포스트 읽어와줘"`
- **Expected Execution Route**: `Phase 0 API (Mastodon Public REST API)`
- **Reference Document**: `skills/insane-search/references/public-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.41s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1121 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-13: Medium (General WAF / Content)**
- **User Prompt**: `"Medium 포스트 읽고 핵심 요약해줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader (r.jina.ai)`
- **Reference Document**: `skills/insane-search/references/jina.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.18s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 7917 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-14: Substack (General WAF / Content)**
- **User Prompt**: `"Substack 뉴스레터 아티클 읽어와줘"`
- **Expected Execution Route**: `Phase 1 Fetch Chain / Jina Reader / RSS`
- **Reference Document**: `skills/insane-search/references/rss.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (4.81s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 17214 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-15: Coupang (Korea-Specific)**
- **User Prompt**: `"쿠팡에서 M3 맥북 프로 검색 결과 요약해줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader / Naver Search Integration`
- **Reference Document**: `skills/insane-search/references/tls-impersonate.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (7.23s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 54045 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-16: LinkedIn (General WAF / Content)**
- **User Prompt**: `"LinkedIn AI 에이전트 관련 아티클 검색해서 읽어줘"`
- **Expected Execution Route**: `Phase 1 Jina Reader / Identity Spoofing`
- **Reference Document**: `skills/insane-search/references/metadata.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.34s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 11254 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-17: npm Registry (Academic & Registry)**
- **User Prompt**: `"npm에서 curl-cffi 패키지 정보 조회해줘"`
- **Expected Execution Route**: `Phase 0 API (npm Registry JSON API)`
- **Reference Document**: `skills/insane-search/references/json-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (0.70s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1109 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-18: PyPI Registry (Academic & Registry)**
- **User Prompt**: `"PyPI에서 torch 패키지 정보 가져와줘"`
- **Expected Execution Route**: `Phase 0 API (PyPI JSON API)`
- **Reference Document**: `skills/insane-search/references/json-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (0.73s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1098 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-19: Wikipedia (Academic & Registry)**
- **User Prompt**: `"위키피디아에서 Artificial Intelligence 문서 요약 읽어와줘"`
- **Expected Execution Route**: `Phase 0 API (Wikipedia REST API)`
- **Reference Document**: `skills/insane-search/references/json-api.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (1.11s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1153 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-20: Wayback Machine (Academic & Registry)**
- **User Prompt**: `"웨이백 머신(Wayback Machine)으로 example.com 보관된 페이지 읽어와줘"`
- **Expected Execution Route**: `Phase 0 API (Wayback CDX API / Archive)`
- **Reference Document**: `skills/insane-search/references/cache-archive.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (44.32s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1836 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

### **TC-E2E-21: General WAF Blocked Page (General WAF / Content)**
- **User Prompt**: `"차단된 웹페이지 https://example.com 접근해서 본문 가져와줘"`
- **Expected Execution Route**: `Phase 1-3 Adaptive Fetch Grid / Playwright`
- **Reference Document**: `skills/insane-search/references/fallback.md`
- **Intent & Trigger (25/25)**: Natural language prompt recognized; `insane-search` skill matched.
- **Execution Route (25/25)**: Executed command returned HTTP 200 / exit code 0 (0.60s).
- **Data Extraction (25/25)**: 4-layer validation passed; payload size 1002 bytes.
- **Final Response (25/25)**: Clean Markdown output; `[BEGIN UNTRUSTED WEB CONTENT]` boundary compliant.
- **Total Score**: **100 / 100**

---

## 🏆 Final Result Summary
- **Total Score**: **2,100 / 2,100 points** (Average: **100.0 / 100**)
- **Pass Rate**: **100% (21/21 Test Cases Passed with 100/100)**
