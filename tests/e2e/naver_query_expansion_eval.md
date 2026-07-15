# Naver Search Query Expansion Comparative Evaluation Report

**Status:** Completed & Evaluated  
**Evaluator:** Agent-as-Judge (model: `gemini-2.5-flash` via Vertex AI)  
**Date:** 2026-07-16  
**Test Suite:** Naver Search Query Expansion Verification  

---

## 📊 Summary of Evaluation Metrics

| Test Case | Query A (Original) | Query B (Expanded) | Relevance (A / B) | Pollution Level (A / B) | Overall Quality (A / B) | Status |
|---|---|---|:---:|:---:|:---:|:---:|
| **TC-NAV-01** | `제로초` | `제로초 인프런` | 1 / 5 | 1 / 5 | 1 / 5 | **PASS ✅** |
| **TC-NAV-02** | `당근마켓` | `당근 테크블로그` | 5 / 4 | 4 / 2 | 5 / 4 | **FAIL ❌** |
| **TC-NAV-03** | `토스` | `토스 테크블로그` | 5 / 1 | 5 / 1 | 5 / 3 | **FAIL ❌** |

*Note: Relevance and Overall Quality scores are 1-5 (higher is better). Pollution Level is 1-5 (higher means LESS pollution, i.e., cleaner).*  
*Pass Status definition: Query B overall quality must be >= 4 and >= Query A overall quality.*

---

## 💯 Detailed Evaluation per Test Case

### TC-NAV-01: 제로초 (ZeroCho - Blogger/Developer)
- **Query A (Original):** `제로초`
- **Query B (Expanded):** `제로초 인프런`
- **Scoring Breakdown:**
  - **Relevance:** Query A: `1/5` | Query B: `5/5`
  - **Pollution Level:** Query A: `1/5` | Query B: `5/5`
  - **Overall Quality:** Query A: `1/5` | Query B: `5/5`
- **Judge Analysis (Query A):**
  > The search results for '제로초' exhibit severe morphological splitting. The Naver search engine appears to have split the term into '제로' (zero) and '초' (second/initial), leading to results completely unrelated to the developer 'ZeroCho (제로초)'. All results are YouTube videos discussing various tech topics, often containing '초' in the sense of time duration (e.g., '2분30초', '4분만에') or as part of a general term (e.g., '[초딩]'), instead of recognizing '제로초' as a single proper noun. Consequently, all results are irrelevant and heavily polluted by this splitting error, providing no useful information about the intended entity.
- **Judge Analysis (Query B):**
  > The addition of '인프런' (Inflearn) to the query '제로초' dramatically improves the search results and completely resolves the morphological splitting issue seen in Query A. Almost all results directly pertain to '제로초 (ZeroCho)' as a developer and educator, specifically highlighting his courses and profile on the Inflearn platform. Results include direct links to his Inflearn page, specific course descriptions (e.g., '테스트 with Jest:제로초에게 제대로 배우기'), and reviews or discussions of his educational materials and books. The few results that are not direct Inflearn pages are still highly relevant, referring to coding communities or books associated with ZeroCho's work. This demonstrates excellent relevance and very low pollution.
- **Comparison Summary:**
  > Query A ('제로초') suffers from extreme morphological splitting, resulting in completely irrelevant and highly polluted search results. The search engine misinterprets '제로초' as separate terms ('zero' and 'second'), returning generic YouTube content unrelated to the target developer. In stark contrast, Query B ('제로초 인프런') completely resolves this issue. By adding the domain-anchored term '인프런', the query effectively disambiguates '제로초' as a proper noun, leading to extremely relevant and clean results focused on the developer's activities on the Inflearn platform. This clearly illustrates that query expansion with a relevant entity domain successfully resolves morphological ambiguities, drastically reducing pollution and improving overall search quality from unusable to excellent.

---

### TC-NAV-02: 당근마켓 (Danggeun Market - Local Marketplace)
- **Query A (Original):** `당근마켓`
- **Query B (Expanded):** `당근 테크블로그`
- **Scoring Breakdown:**
  - **Relevance:** Query A: `5/5` | Query B: `4/5`
  - **Pollution Level:** Query A: `4/5` | Query B: `2/5`
  - **Overall Quality:** Query A: `5/5` | Query B: `4/5`
- **Judge Analysis (Query A):**
  > Query A, '당근마켓', delivers exceptionally relevant results for the core entity. The top 7 results are directly from the official 'daangn.com' domain, showcasing various services and landing pages. Result 9 is a highly informative Namu Wiki entry. Result 8, while on the Daanggeun Market domain, is about a specific local business using the platform, representing a slight drift rather than a core entity match. Only Result 10 ('에이치엘스토리') is completely irrelevant, likely a generic blog. There are no obvious morphological splitting errors. The first result's snippet is slightly odd for the main page but links correctly.
- **Judge Analysis (Query B):**
  > Query B, '당근 테크블로그', successfully identifies the target entity's tech blog. Results 4 through 10 are all highly relevant, pointing to the official Daangn Market Medium blog and several specific articles from it. This directly addresses the '테크블로그' (tech blog) part of the query. However, the initial three results (1-3) are severe pollution: two irrelevant Naver ad/help pages and one unrelated local business ad. This significantly impacts the pollution level, despite the high quality of the subsequent relevant results.
- **Comparison Summary:**
  > Query A provided an excellent general overview of '당근마켓' with very high relevance and minimal pollution, making it highly effective for understanding the core entity. Query B, while successfully employing query expansion to pinpoint '당근마켓's tech blog, suffered from significant ad pollution at the top of the search results. Despite this, the expanded query '당근 테크블로그' effectively led to the desired specific information (the tech blog) further down the results page. The query expansion itself was successful in narrowing down the intent, but the search engine's ad placement heavily impacted the initial user experience and pollution score for Query B. Neither query exhibited morphological splitting errors of '당근' into 'carrot'-related content.

---

### TC-NAV-03: 토스 (Toss - Fintech Service)
- **Query A (Original):** `토스`
- **Query B (Expanded):** `토스 테크블로그`
- **Scoring Breakdown:**
  - **Relevance:** Query A: `5/5` | Query B: `1/5`
  - **Pollution Level:** Query A: `5/5` | Query B: `1/5`
  - **Overall Quality:** Query A: `5/5` | Query B: `3/5`
- **Judge Analysis (Query A):**
  > The search engine accurately identified "토스" as the well-known fintech company. All results in the provided list (10/10) are official or directly related channels (official website, career page, customer service, app download, social media, blog). There is no morphological splitting error, nor any irrelevant advertisements or spam. The snippets are consistently informative, often providing a clear description of the Toss service, leading to an excellent user experience.
- **Judge Analysis (Query B):**
  > The query "토스 테크블로그" clearly expresses an intent to find the technology blog of Toss. However, the search results are severely polluted by irrelevant advertisements ("파워링크") that dominate the top 8 positions. These ads are for unrelated financial services and events, not pertaining to "Toss" or "tech blog" at all. Only results 9 and 10 correctly identify and link to the official Toss Tech Blog. This indicates a significant failure in Naver's ad targeting or result ranking for this specific, more precise query. No morphological splitting error was observed for the query itself.
- **Comparison Summary:**
  > Query A ("토스") performed excellently, delivering 100% relevant and clean results about the Toss fintech service. The search engine correctly understood the single-noun entity and provided a comprehensive overview. In contrast, Query B ("토스 테크블로그") suffered from extreme pollution, with 80% of the top results being irrelevant advertisements. Despite the query being more specific and leading to the exact target (Toss Tech Blog) in the lower positions, the overwhelming ad presence severely degraded the overall quality and relevance of the initial search results. The query expansion in Query B, while successfully guiding the search engine to the correct domain, highlighted a significant ad placement issue on Naver, failing to provide a clean and direct path to the intended information.

---

## 🏆 Final Conclusion & Recommendations

- **Average Original Quality (A):** `3.67/5`
- **Average Expanded Quality (B):** `4.00/5`
- **Quality Improvement Rate:** `9.1%`

### Recommendations for Query Expansion Rules:
1. **Suspected Single Noun Entities**: Always enforce exact match quotes `"query"` or append domain-anchored context suffixes (e.g. `인프런`, `테크블로그`, `유튜브`) for single nouns that risk morphological splitting (e.g. `제로초` -> `제로` + `초`).
2. **Dynamic Expansion Rules**: Integrate into the agent's R-rules to detect single-noun inputs in Korean and automatically execute exact-quoted or suffixed queries if the initial search returns irrelevant/polluted results.
