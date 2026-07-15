# Test Plan: Refactored `insane-search` Skill (AGY 2.0 Environment)

**Version**: 2.0  
**Role**: Product Manager & Test Scenario Planner  
**Target Repository**: [skills/insane-search](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search)  
**Environment**: Antigravity (AGY) 2.0 CLI & Multi-Agent Ecosystem  

---

## 1. Executive Summary & Core Testing Principles

The refactored `insane-search` skill provides adaptive, resilient access to blocked or protected websites by automating escalation across Phase 0 official APIs, generic WAF profile grids (`curl_cffi` TLS impersonation, URL transformations, referer strategies), and Playwright fallbacks.

### Key Architectural Rules & Invariants
1. **R1 — Single Entrypoint**: All web fetch operations execute via `python3 -m engine "<URL>"` or `from insane_search.engine import fetch`.
2. **R2 — 4-Layer Validation**: HTTP 200 is only a check prerequisite. Pass requires 4 layers: no challenge markers, body size $\ge$ 3KB (unless selector specified), cookie sensor valid, and optional positive-proof CSS selectors matched.
3. **R3 — No-Site-Name Rule**: Zero site domain/brand hardcoding in `engine/**` or `waf_profiles.yaml`. CI verified via [engine/bias_check.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/bias_check.py).
4. **R5 — Phase 0 Official API First**: Deterministic routing for platforms with open/official APIs (Reddit RSS, X/Twitter syndication/oEmbed, YouTube yt-dlp, arXiv, HN).
5. **R6 — Failure Gate Enforcement**: Premature "blocked" declaration is blocked unless `grid_exhausted=true`, `untried_routes=[]`, `must_invoke_playwright_mcp=false`, and `stop_reason` is terminal (`auth_required`, `404`, `paywall`).
6. **R7 — WAF Early Detection & API-First Split**: Triggers on 2–3 consecutive `verdict=challenge` with known WAF profiles during list/bulk scraping, recommending background grid execution alongside MCP Playwright network inspection.
7. **R8 — Untrusted Web Boundary Control**: Web content wrapped in `[BEGIN UNTRUSTED WEB CONTENT]` with unique boundary ID and prompt injection risk evaluation.

---

## 2. Structured Test Plan Matrix

| Scenario ID | Category | Scenario Name | Primary Component / Module |
|---|---|---|---|
| **SC-01** | WAF & Blocked Sites | Generic Fetch Grid & TLS Impersonation | [engine/fetch_chain.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/fetch_chain.py), [engine/waf_detector.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/waf_detector.py) |
| **SC-02** | Phase 0 Official API | Deterministic Platform API Routers | [engine/phase0.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/phase0.py) |
| **SC-03** | CLI Execution | Python CLI Entrypoint & Argument Handling | [engine/__main__.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/__main__.py) |
| **SC-04** | Error Handling & Gates | R6 Failure Gates, R7 Split, R8 Untrusted Boundary | [engine/validators.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/validators.py), [engine/content_safety.py](file:///Users/jjinseo/gcp-handson/insane-search-agy/skills/insane-search/engine/content_safety.py) |

---

## 3. Detailed Test Scenarios & Pass/Fail Criteria

### Scenario 1: WAF / Blocked Website Access
**Objective**: Verify adaptive access to protected websites (e.g., Naver Blog, Medium, Reddit web HTML, protected e-commerce) using site-agnostic TLS impersonation grids, URL transformations, and Playwright fallbacks.

#### Test Case 1.1: Naver Blog / Korean Portal Access
* **Target URL**: `https://blog.naver.com/...` or `https://m.blog.naver.com/...`
* **Test Command**:
  ```bash
  python3 -m engine "https://m.blog.naver.com/" --selector "main" --trace
  ```
* **Pre-conditions**: Network connectivity active; `curl_cffi >= 0.15.0` installed.
* **Execution Steps**:
  1. Engine probes main URL with Safari impersonation and `self_root` Referer.
  2. Evaluates `url_transforms` (`mobile_subdomain`, `original`).
  3. Validates 4-layer check against challenge markers and body size.
* **Expected Result**:
  - `ok`: `True`
  - `verdict`: `strong_ok` (if selector matched) or `weak_ok`
  - `trace`: Shows probe/grid attempts with HTTP 200 and clean HTML response (> 3KB).
* **Pass Criteria**: Engine successfully retrieves blog content without hitting captcha/block pages; no site-specific code executed.
* **Fail Criteria**: Exit code `1`, `verdict=challenge`, or failure to transform mobile URLs.

#### Test Case 1.2: Medium Article / Cloudflare Shielded Site Access
* **Target URL**: `https://medium.com/@username/article-slug`
* **Test Command**:
  ```bash
  python3 -m engine "https://medium.com" --device desktop --json
  ```
* **Pre-conditions**: Medium returns Cloudflare turnstile / challenge to plain HTTP clients.
* **Execution Steps**:
  1. Initial probe hits Cloudflare challenge marker (`verdict=challenge`).
  2. WAF Detector identifies `cloudflare_turnstile` profile.
  3. Executor runs impersonation grid (`chrome131`, `safari`, `firefox`).
  4. If TLS impersonation fails, triggers Playwright fallback (`playwright_real_chrome.js` or MCP).
* **Expected Result**:
  - `ok`: `True`
  - `profile_used`: `cloudflare_turnstile`
  - JSON output contains valid trace log and fetched content.
* **Pass Criteria**: HTTP 200 containing article body; 4-layer validation passes; no unhandled exceptions.
* **Fail Criteria**: Premature exit on initial HTTP 200 challenge page; `ok=False` while `untried_routes` remains non-empty.

#### Test Case 1.3: E-Commerce / Akamai Protected Site
* **Target URL**: Generic protected e-commerce domain (e.g., Coupang, SSG, or test WAF endpoint).
* **Test Command**:
  ```bash
  python3 -m engine "https://www.coupang.com/" --device auto --trace
  ```
* **Execution Steps**:
  1. Probe fails with Akamai Bot Manager challenge.
  2. Profile detected as `akamai_bot_manager` (`capabilities_needed`: `needs_real_tls_stack`, `needs_js_exec`).
  3. Executor selects local Node Playwright with system Chrome channel (`playwright_real_chrome.js`).
* **Expected Result**:
  - `ok`: `True`
  - `executor`: `playwright_real_chrome`
  - `verdict`: `weak_ok` or `strong_ok`
* **Pass Criteria**: Bypasses Akamai JavaScript challenge via Chrome TLS stack; returns full rendered page.
* **Fail Criteria**: Engine attempts plain `curl` repeatedly without escalating to Playwright; returns `verdict=challenge`.

---

### Scenario 2: Phase 0 Official API Router Execution
**Objective**: Validate deterministic pre-grid execution for platforms with official open APIs (YouTube, Reddit, arXiv, X/Twitter, Hacker News).

#### Test Case 2.1: YouTube Metadata & Subtitles (`yt-dlp` Router)
* **Target URL**: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
* **Test Command**:
  ```bash
  python3 -m engine "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --json
  ```
* **Execution Steps**:
  1. `phase0.route()` detects `youtube` platform.
  2. Invokes `yt-dlp --dump-json --skip-download`.
  3. Intercepts response before generic WAF grid execution.
* **Expected Result**:
  - `ok`: `True`
  - `platform`: `youtube`
  - `route`: `yt-dlp`
  - `content`: Valid JSON string with video ID, title, uploader, and description.
* **Pass Criteria**: Returns in under 3 seconds via `yt-dlp`; generic WAF grid is **not** invoked (`trace` has 1 entry with `phase=phase0`).
* **Fail Criteria**: Falls through to web HTML scraping when `yt-dlp` is installed and functional.

#### Test Case 2.2: Reddit Subreddit / Post Access (RSS Router)
* **Target URL**: `https://www.reddit.com/r/Python/`
* **Test Command**:
  ```bash
  python3 -m engine "https://www.reddit.com/r/Python/" --trace
  ```
* **Execution Steps**:
  1. `phase0.route()` detects `reddit` platform.
  2. Transforms URL to `.rss` feed (`https://www.reddit.com/r/Python/.rss`).
  3. Executes `curl_cffi` GET with Safari impersonation.
* **Expected Result**:
  - `ok`: `True`
  - `platform`: `reddit`
  - `route`: `rss`
  - `content`: Contains `<rss>` or `<feed>` XML tags with latest post entries.
* **Pass Criteria**: Successfully retrieves RSS feed avoiding Reddit 403 WAF blocks on `.json` or HTML endpoints.
* **Fail Criteria**: Receives 403 Forbidden or falls back to scraping Reddit HTML grid without trying `.rss`.

#### Test Case 2.3: arXiv Research Paper Metadata
* **Target URL**: `https://arxiv.org/abs/2301.00001`
* **Test Command**:
  ```bash
  python3 -m engine "https://arxiv.org/abs/2301.00001" --json
  ```
* **Execution Steps**:
  1. Intercepted via Phase 0 / Public API router.
  2. Requests arXiv Atom API (`https://export.arxiv.org/api/query?id_list=2301.00001`).
* **Expected Result**:
  - `ok`: `True`
  - `content`: XML payload containing paper title, abstract, authors, and primary category.
* **Pass Criteria**: Paper metadata returned cleanly without scraping HTML.
* **Fail Criteria**: Network error or missing paper abstract.

---

### Scenario 3: CLI Python Engine Invocation
**Objective**: Test CLI flags, output formats, device pinning, trace formatting, and exit codes.

#### Test Case 3.1: Standard CLI Fetch with Selector
* **Command**:
  ```bash
  python3 -m engine "https://example.com" --selector "h1"
  ```
* **Expected Output**:
  - `stdout`: Page HTML text containing `<h1>Example Domain</h1>`.
  - `stderr`: `[engine] ok=True verdict=strong_ok profile=unknown attempts=1`
  - `exit code`: `0`
* **Pass Criteria**: Exit code `0`; `strong_ok` reported due to selector match.

#### Test Case 3.2: JSON Schema Output Mode
* **Command**:
  ```bash
  python3 -m engine "https://example.com" --json
  ```
* **Expected Output**:
  - `stdout`: Valid JSON object matching `FetchResult.to_dict()`:
    ```json
    {
      "ok": true,
      "verdict": "weak_ok",
      "profile_used": "unknown",
      "stop_reason": null,
      "grid_exhausted": true,
      "untried_routes": [],
      "must_invoke_playwright_mcp": false,
      "trace": [...]
    }
    ```
* **Pass Criteria**: Clean JSON output parseable by `jq` / `json.loads()`; exit code `0`.

#### Test Case 3.3: Mobile Device Pinning & Trace Output
* **Command**:
  ```bash
  python3 -m engine "https://example.com" --device mobile --trace
  ```
* **Expected Output**:
  - `stderr`: Prints `=== trace ===` section detailing transform (`mobile_subdomain`), impersonation (`safari_ios` / `chrome_android`), HTTP status, body size, and verdict.
* **Pass Criteria**: Mobile UAs and mobile URL transforms strictly applied; trace printed to stderr.

#### Test Case 3.4: Disabling Phase 0 and Playwright
* **Command**:
  ```bash
  python3 -m engine "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --no-phase0 --no-playwright --trace
  ```
* **Pass Criteria**: Phase 0 bypass confirmed (trace shows generic grid attempts, no `yt-dlp`); Playwright fallback suppressed.

---

### Scenario 4: Error Handling & R6 Failure Gates Verification
**Objective**: Ensure system safety, failure gate enforcement, escalation compliance, and security sanitization.

#### Test Case 4.1: R6 Failure Gate Enforcement (`⛔ NOT EXHAUSTED`)
* **Setup**: Run CLI with artificially constrained attempt budget on a protected site.
* **Command**:
  ```bash
  python3 -m engine "https://medium.com" --max-attempts 1 --no-playwright
  ```
* **Expected Output**:
  - `exit code`: `1`
  - `stderr`:
    ```text
    ════════════════════════════════════════════════════════════════
    ⛔ NOT EXHAUSTED — do not declare failure yet (R6).
       grid_exhausted=False  stop_reason=None
       Routes the engine cannot run itself — try these before giving up:
         • device_class=mobile
         • referer_strategy=none
       ➜ must_invoke_playwright_mcp = TRUE — drive MCP Playwright from the agent session.
    ════════════════════════════════════════════════════════════════
    ```
* **Pass Criteria**: CLI outputs prominent `NOT EXHAUSTED` warning; returns non-empty `untried_routes` and `must_invoke_playwright_mcp=True`.
* **Fail Criteria**: Engine returns `ok=False` and allows agent to conclude "site is blocked" without signaling unattempted routes.

#### Test Case 4.2: Terminal Error Recognition (404 / 401 Auth Required)
* **Command**:
  ```bash
  python3 -m engine "https://httpbin.org/status/404" --json
  ```
* **Expected Result**:
  - `ok`: `False`
  - `stop_reason`: `404` (or `terminal`)
  - `untried_routes`: `[]` (empty list)
  - `must_invoke_playwright_mcp`: `False`
* **Pass Criteria**: Engine recognizes terminal HTTP status, clears `untried_routes`, and does **not** output `NOT EXHAUSTED` warning.
* **Fail Criteria**: Classifies 404 as a temporary WAF challenge or retries indefinitely.

#### Test Case 4.3: R7 Early WAF Detection & API-First Guidance
* **Setup**: Trigger 2–3 consecutive `verdict=challenge` responses on an Akamai or Cloudflare site.
* **Expected Result**:
  - `summary`: Contains `R7 API-first` guidance recommendation.
  - `stderr`: Displays banner:
    `⚠️ R7 triggered — consider API-first route instead of HTML grid.`
  - Directs Agent to run engine in background (`run_in_background=true`) while performing MCP Playwright XHR/fetch network inspection.
* **Pass Criteria**: R7 banner and guidance displayed prominently when condition met.

#### Test Case 4.4: R8 Untrusted Content Boundary & Prompt Injection Detection
* **Setup**: Fetch target containing adversarial instructions (e.g. prompt injection payloads).
* **Execution Steps**: Inspect text output from `result.to_untrusted_text()`.
* **Expected Result**:
  - Output enclosed within `[BEGIN UNTRUSTED WEB CONTENT <uuid>]` and `[END UNTRUSTED WEB CONTENT <uuid>]`.
  - `prompt_injection_risk`: `medium` or `high` logged to stderr when signals detected.
* **Pass Criteria**: Content strictly isolated; prompt injection signals surfaced in metadata.

#### Test Case 4.5: Codebase Bias Linter Compliance (CI Gate)
* **Command**:
  ```bash
  python3 skills/insane-search/engine/bias_check.py
  ```
* **Expected Output**: `[bias-check] ✅ clean`
* **Pass Criteria**: Exit code `0`; 0 brand/domain name violations in `engine/` or `waf_profiles.yaml`.

---

## 4. Test Execution Summary Checklist

- [x] **Smoke Test Battery**: `python3 skills/insane-search/engine/tests/test_smoke.py` (8/8 Passed)
- [x] **Bias Check Linter**: `python3 skills/insane-search/engine/bias_check.py` (Clean)
- [ ] **Scenario 1 Verification**: WAF & Blocked Site Fetch Grid
- [ ] **Scenario 2 Verification**: Phase 0 Routers (YouTube `yt-dlp`, Reddit RSS, arXiv)
- [ ] **Scenario 3 Verification**: CLI Engine Invocation & Output Options
- [ ] **Scenario 4 Verification**: R6 Failure Gates, R7 API-First Split, R8 Security Boundary

---
*Document generated by Jetski Agent (Product Manager & Test Scenario Planner).*
