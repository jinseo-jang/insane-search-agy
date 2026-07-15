# Insane Search: Future Architectural Proposals and Recommendations

This document outlines future architectural proposals and recommendations for the `insane-search` engine to enhance its resiliency, flexibility, and evasion capabilities against advanced Web Application Firewalls (WAFs) and bot managers.

---

## Executive Summary

The `insane-search` engine utilizes a multi-layered approach to bypass WAF challenges, starting with official API routes (Phase 0), escalating to a diverse TLS/transform/referer attempt grid (Phase 1), and falling back to capability-matched Playwright automation (Phase 3). 

To ensure long-term viability and handle increasingly sophisticated bot-management heuristics (such as dynamic DOM restructuring, TLS fingerprint blacklisting, and IP reputation tracking), we propose five core architectural advancements:
1. **Dynamic Selector Discovery via LLM-in-the-Loop**: Resolving selector fragility dynamically via context-aware LLMs.
2. **Adaptive Proxy and Session Rotation Grid**: Integrating residential, datacenter, and mobile proxies as primary axes in the scheduling grid.
3. **Advanced Playwright Cookie Sharing & Session Persistence**: Utilizing persistent `storageState` contexts and bi-directional cookie bridges to optimize browser fallback overhead.
4. **Expansion of Phase 0 to Regional Platforms**: Adding dedicated routers and REST API targets for South Korean portals (Daum, Kakao, DCInside).
5. **Decentralized Multi-Agent Node Fallbacks**: Cooperatively distributing fetch operations to adjacent nodes within a peer-to-peer agent network.

---

## 1. Dynamic Selector Discovery via LLM-in-the-Loop

### Problem Statement
Modern Single Page Applications (SPAs) and e-commerce platforms frequently update their DOM structure, class names, and element hierarchies. This often includes using CSS-in-JS libraries that compile classes into unstable hashes (e.g., `.sc-bczRLJ`). When static `success_selectors` fail due to DOM changes, `insane-search` incorrectly classifies a successful HTTP 200 clean response as a WAF challenge (`Verdict.CHALLENGE` with reason `"no_success_selector"`), resulting in unnecessary fallbacks and higher latency.

### Proposed Architecture
We propose introducing a dynamic selector discovery mechanism that runs as a recovery sub-phase within `validators.py` and `fetch_chain.py`. When a selector mismatch occurs on an otherwise clean response, the DOM is minified and sent to a fast, context LLM to discover the correct CSS selector dynamically.

```
+------------------+     validate()     +--------------------+
|  Fetch Response  | -----------------> | Verdict.CHALLENGE  |
+------------------+                    | no_success_selector|
         |                              +--------------------+
         |                                        |
         | (Fallback Triggered)                   v
         |                              +--------------------+
         |                              | Minify DOM HTML    |
         |                              +--------------------+
         |                                        |
         |                                        v
         |                              +--------------------+
         |                              | Ask LLM: Find CSS  |
         |                              | Selector for Query |
         |                              +--------------------+
         |                                        |
         v                                        v
+------------------+   Re-validate()    +--------------------+
|  STRONG_OK /     | <----------------- | Apply New Selector |
|  WEAK_OK         |                    +--------------------+
+------------------+
         |
         v
+-----------------------------+
| Cache Selector in           |
| learning.py & Session State |
+-----------------------------+
```

### Technical Design & Implementation Blueprint
1. **DOM Minification Filter**:
   Before sending the page HTML to the LLM, the engine must strip elements that do not contribute to structure (e.g., `<script>`, `<style>`, `<svg>`, `<iframe>`, `<img>`, comment blocks, and raw inline text nodes beyond a short length). This minimizes token usage and fits within restricted context windows.
2. **LLM Prompt Schema**:
   The prompt describes the user's intent (what they were attempting to extract) and provides the structural minified DOM. The LLM must output a valid CSS selector inside a structured JSON schema.
3. **Integration into `validators.py`**:
   Extend `validate()` to return a distinct status indicating that the DOM structure was successfully loaded but selectors did not match.
4. **Integration into `fetch_chain.py`**:
   Implement a recovery loop:
   ```python
   # Pseudo-code inside fetch_chain.py
   vr = validate(resp, success_selectors=success_selectors)
   if vr.verdict == Verdict.CHALLENGE and "no_success_selector" in vr.reasons:
       # Trigger LLM-in-the-loop recovery
       minified_dom = minify_dom(resp.text)
       new_selector = query_llm_for_selector(minified_dom, user_intent_hint)
       if new_selector:
           # Re-validate with the discovered selector
           vr = validate(resp, success_selectors=[new_selector])
           if vr.ok:
               # Cache the winning selector for the host to prevent future LLM calls
               learning.record_selector(url, new_selector)
   ```

---

## 2. Adaptive Proxy and Session Rotation Grid

### Problem Statement
Bot managers like Akamai and Kasada categorize incoming IP addresses into reputation tiers. Datacenter IPs are blocked instantly, while residential and mobile IPs are monitored with lower suspicion levels. Currently, `insane-search` operates on a single local IP or a static proxy, which limits its ability to evade strict IP-based rate limiting and reputation blocklists.

### Proposed Architecture
We propose integrating an adaptive proxy grid where residential, datacenter, and mobile proxies are classified into distinct tiers and mapped directly within the WAF product profiles in `waf_profiles.yaml`. The diversity planner in `fetch_chain.py` will then treat proxies as a scheduling axis, matching proxy tiers to the identified bot manager.

```
                   +------------------------------+
                   |     waf_profiles.yaml        |
                   |                              |
                   |  akamai_bot_manager:         |
                   |    preferred_proxy_tier:      |
                   |      - mobile                |
                   |      - residential           |
                   +------------------------------+
                                  |
                                  v
+------------------+     Select Profile         +---------------------+
|   WAF Detected   | -------------------------> |  Diversity Planner  |
+------------------+                            +---------------------+
                                                           |
                                                           | Schedule Attempts
                                                           v
                                                +---------------------+
                                                | attempt 1: mobile   |
                                                | attempt 2: res.     |
                                                | attempt 3: DC       |
                                                +---------------------+
```

### Technical Design & Implementation Blueprint
1. **`waf_profiles.yaml` Schema Extension**:
   ```yaml
   akamai_bot_manager:
     detectors: ...
     capabilities_needed:
       - needs_real_tls_stack
       - needs_js_exec
     preferred_proxy_tier:
       - mobile          # Highest cost, highest trust; try first for Akamai
       - residential     # Medium cost, high trust
       - datacenter      # Low cost; deprioritized for Akamai
     fallback_when_challenge:
       - playwright_real_chrome
   ```
2. **Diversity Planner Updates (`fetch_chain.py`)**:
   Modify `_plan_for_profile` and `_build_plan` to inject the proxy configuration as a dimension in the scheduling grid. The candidate selection alternates between TLS families, URL transforms, and proxy tiers to ensure maximum diversity across early attempts.
3. **SessionPool Updates (`transport.py`)**:
   The `SessionPool` must manage persistent TCP connections *per proxy endpoint* to avoid the overhead of constant TLS handshakes.
   ```python
   # Proposed interface in transport.py
   class ProxySessionPool:
       def request(self, url, impersonate, referer, proxy_tier, timeout):
           proxy_url = self.get_next_proxy(proxy_tier)
           # Reuse or spawn a curl_cffi Session routed through proxy_url
           session = self.get_session(proxy_url, impersonate)
           return session.get(url, referer=referer, timeout=timeout)
   ```

---

## 3. Advanced Playwright Cookie Sharing & Session Persistence

### Problem Statement
When the Python `curl_cffi` grid fails, the engine falls back to browser automation (Playwright). Running a full headless browser is computationally heavy, and resolving dynamic challenges (like Cloudflare Turnstile or Akamai sensor challenges) takes several seconds. Currently, `insane-search` uses a hashed directory per host to isolate profiles, but does not persist session cookies bi-directionally or reuse context state efficiently across separate execution runs.

### Proposed Architecture
We propose implementing a persistent context model using Playwright's `storageState` along with a bi-directional cookie bridge between the Python `curl_cffi` transport layer and the Node.js Playwright instance. This minimizes the need to solve challenges repeatedly and warms HTTP sessions immediately.

```
+----------------------+                       +----------------------+
|  curl_cffi Session   |                       |  Playwright Browser  |
|  (SessionPool)       |                       |  (storageState.json) |
+----------------------+                       +----------------------+
           |                                               |
           | 1. Export cookies                             |
           +---------------------> [Bridge] --------------->
                                                           | 2. Restores warm
                                                           |    session state
                                                           v
                                                   [Solves WAF Challenge]
                                                           |
                                                           | 3. Exports new 
           <--------------------- [Bridge] <---------------+    cookies & UA
           |
           v
  4. Seeds curl pool
     (Subsequent fetches
      bypass browser!)
```

### Technical Design & Implementation Blueprint
1. **Persistent Context Storage**:
   Use Playwright's `browserContext.storageState({ path: 'storageState.json' })` to serialize cookies and localStorage. Store this file in the hashed profile directory defined by `_profile_dir_for(url, choice)` in `executor.py`.
2. **Bi-Directional Bridge Execution Flow**:
   - **Python to Node**: Before launching the Playwright subprocess, extract cookies for the target host from the Python `POOL` session. Generate/update the target host's `storageState.json` file.
   - **Node execution**: The JS template loads the storage state:
     ```javascript
     // Inside templates/playwright_real_chrome.js
     const context = await browser.newContext({
       storageState: args.storageStatePath,
       userAgent: args.userAgent
     });
     ```
   - **Node to Python**: After a successful page load, the JS script writes the final cookies, localStorage, and User-Agent as a JSON envelope to `stdout`. The Python `run_playwright_fallback` parses this envelope and calls `_bridge_cookies_to_pool` to update the active `curl_cffi` connections.

---

## 4. Expansion of Phase 0 to Regional Platforms (South Korea Focus)

### Problem Statement
South Korean news portals, finance hubs, and community platforms (e.g., Kakao News, Daum Finance, DCInside) employ custom structures, highly dynamic rendering engines, and localized anti-bot guards. Accessing these portals via the generic WAF grid is slow and error-prone. However, these platforms often expose lightweight endpoints (mobile subdomains, oEmbed providers, and internal REST APIs) that can be targeted deterministically.

### Proposed Architecture
We propose expanding the Phase 0 API router (`phase0.py`) with specialized adapters for South Korean platforms. Since Phase 0 executes before the generic grid, these platforms will bypass WAF detection entirely, reducing latency and resource consumption.

```
                     +---------------------------------------+
                     |            phase0.py                  |
                     |                                       |
                     |  Is URL matches South Korean portal?  |
                     +---------------------------------------+
                        /                 |                 \
                       /                  |                  \
                      v                   v                   v
             +--------------+     +---------------+     +--------------+
             |  DCInside    |     |  Daum Finance |     |  Kakao News  |
             +--------------+     +---------------+     +--------------+
              Mobile redirect      Internal REST API     oEmbed & RSS 
              & RSS fetching       w/ referer bypass     extraction
```

### Technical Design & Implementation Blueprint
1. **Daum/Kakao Finance REST API Integration**:
   Direct stock quote requests (e.g., `https://finance.daum.net/quotes/A005930`) to their internal JSON endpoint:
   - Endpoint: `https://finance.daum.net/api/quotes/A005930`
   - Requirement: Set referer header to `https://finance.daum.net` and TLS impersonation to `chrome`.
2. **DCInside Mobile redirection & RSS**:
   Redirect standard board requests (e.g., `https://gall.dcinside.com/mgallery/board/view/?id=...`) to mobile-web endpoints (`https://m.dcinside.com/board/...`) or fallback to public feed XML endpoints if available.
3. **Kakao News / Daum News oEmbed**:
   Resolve news URLs through the Daum oEmbed endpoint:
   - Endpoint: `https://news.daum.net/api/oembed?url={URL}`
4. **Platform Support in `phase0.py`**:
   Extend platform detectors and routers in `skills/insane-search/engine/phase0.py`:
   ```python
   def _detect(url: str) -> Optional[str]:
       h = _host(url)
       # ... existing checks ...
       if "dcinside.com" in h:
           return "dcinside"
       if "finance.daum.net" in h:
           return "daum_finance"
       if "news.v.daum.net" in h or "v.daum.net" in h:
           return "daum_news"
       return None
   ```
5. **No-Site-Name Compliance**:
   Phase 0 is the *sanctioned exception* to the No-Site-Name rule. These new routers must be added exclusively inside `phase0.py` to ensure the core WAF grid engine remains fully site-agnostic.

---

## 5. Decentralized Multi-Agent Node Fallbacks

### Problem Statement
When targeting highly secured domains, all local attempts (including browser fallbacks and proxy rotations) may fail if the client's subnet gets flagged. While commercial proxy rotation solves this, it can be expensive and easily identified by IP intelligence databases. 

### Proposed Architecture
In a multi-agent deployment, agents operate on separate nodes (e.g., distinct VMs, local machines, or cloud environments) with different IP subnets. We propose a decentralized P2P request forwarding mechanism. If a local node becomes completely blocked (`grid_exhausted=true`), it routes the request to adjacent agent nodes in the network as a final fallback layer.

```
+------------------------+                    +------------------------+
| Local Node (IP Blocked) |                    | Peer Node (Clean IP)   |
+------------------------+                    +------------------------+
            |                                             |
            | 1. Delegate Request (JSON envelope)         |
            +-------------------------------------------->|
            |                                             | 2. Run insane-search
            |                                             |    engine locally
            |                                             v
            |                                   [Fetch Success]
            |                                             |
            | 3. Return payload (HTML, cookies)           |
            |<--------------------------------------------+
            v
   Return HTML content
   to caller context!
```

### Technical Design & Implementation Blueprint
1. **Delegation Payload Schema**:
   The calling node compiles the execution context into a JSON envelope:
   ```json
   {
     "url": "https://example.com/target",
     "success_selectors": ["article"],
     "device_class": "auto",
     "user_hint": {
       "impersonate_first": "safari"
     }
   }
   ```
2. **P2P Node Communication**:
   Introduce a communication layer in the Multi-Agent framework where nodes query a registry of adjacent healthy nodes.
3. **Execution Logic Flow in `fetch_chain.py`**:
   - When `fetch()` runs and exhausts both the curl grid and Playwright local fallback without success, check if adjacent nodes are registered.
   - Forward the request envelope to the next available peer node via a secure internal API endpoint.
   - The peer node runs the request through its own `insane-search` engine instance and returns the result.
   - The local node imports the returned content, updates its connection pool with the new cookies, and returns success to the user.

---

## Expected Benefits & Performance Metrics

| Proposed Capability | Primary Metric Impact | Evasion Success | Latency / Overhead |
|---|---|---|---|
| **Dynamic Selector Discovery** | Reduces false-positives on selector mismatches | +15% reliability on dynamically updated SPA portals | Overhead of single context-LLM call (~800ms) only on first fail |
| **Adaptive Proxy Grid** | Evades IP-based reputation blocks | Bypasses strict Akamai/Kasada IP blocks | Negotiated connection setup offset via `SessionPool` |
| **Session Persistence** | Eliminates repeated JS/WAF challenges | Bypasses recurring interactive page challenge gates | Saves up to 80% CPU/Memory overhead by reusing warm contexts |
| **Regional Phase 0 Expansion** | Zero-WAF API-first delivery for SK portals | 100% bypass on supported regional portals | Reduces page load latency from 5+ seconds to sub-500ms |
| **P2P Agent Fallbacks** | Distributes request load across subnets | Resolves absolute IP/subnet blockades | Network hop latency (~200ms) |
