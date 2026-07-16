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
| **TC-NAV-02** | `당근마켓` | `당근 테크블로그` | 5 / 4 | 5 / 3 | 5 / 3 | **FAIL ❌** |
| **TC-NAV-03** | `토스` | `토스 테크블로그` | 5 / 1 | 5 / 1 | 5 / 1 | **FAIL ❌** |

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
  > The search engine appears to have performed morphological splitting on '제로초', interpreting '제로' (zero) and '초' (second/initial) independently. This has led to a list of completely unrelated YouTube videos, many of which contain time durations (e.g., '2분30초', '4분만에') where '초' means 'second'. There is no mention or indication of '제로초 (ZeroCho - Blogger/Developer)' in any of the results, making them entirely irrelevant to the intended entity.
- **Judge Analysis (Query B):**
  > Adding '인프런' (Inflearn) as a domain anchor completely resolved the morphological splitting issue seen in Query A. The results are overwhelmingly focused on '제로초 (조현영)', his lectures on Inflearn, his books, and reviews/discussions about his educational content. The top results provide direct links to his Inflearn profile, specific courses, and blog posts detailing user experiences with his teaching. This indicates a strong understanding by the search engine of the user's intent.
- **Comparison Summary:**
  > Query A suffered from severe morphological splitting, where '제로초' was incorrectly parsed as 'zero' and 'second/initial', leading to completely irrelevant results (YouTube videos with time durations). The pollution level was extreme, and the overall quality was unusable for understanding the target entity. Query B, by adding '인프런' as a domain anchor, successfully resolved the morphological splitting problem. The search results became highly relevant, directly pointing to information about '제로초 (ZeroCho - Blogger/Developer)' and his educational content on the Inflearn platform. This query expansion dramatically reduced pollution and significantly improved the overall quality, making the results excellent and highly informative for an AI agent. This demonstrates the critical role of providing disambiguating context in search queries, especially for terms that can be morphologically split or have multiple meanings.

---

### TC-NAV-02: 당근마켓 (Danggeun Market - Local Marketplace)
- **Query A (Original):** `당근마켓`
- **Query B (Expanded):** `당근 테크블로그`
- **Scoring Breakdown:**
  - **Relevance:** Query A: `5/5` | Query B: `4/5`
  - **Pollution Level:** Query A: `5/5` | Query B: `3/5`
  - **Overall Quality:** Query A: `5/5` | Query B: `3/5`
- **Judge Analysis (Query A):**
  > For Query A ('당근마켓'), the search results are overwhelmingly relevant to the target entity '당근마켓 (Danggeun Market - Local Marketplace)'. The top results are direct links to the official Daangn Market website and its various sub-sections (jobs, community, etc.). A highly informative Namu Wiki entry provides a comprehensive overview of the company. Only one result (a general Naver blog without a snippet) seems to be an outlier. There are no signs of morphological splitting (e.g., results about carrots or unrelated markets) or prominent advertisements. The results provide excellent, clean, and direct information about the entity.
- **Judge Analysis (Query B):**
  > For Query B ('당근 테크블로그'), the query expansion successfully targeted the technology blog of '당근마켓'. Results 4 through 10 are all highly relevant, pointing to the official Daangn Market tech blog on Medium and specific articles from it. These results provide exactly the type of detailed technical insights an AI agent might seek. However, the first three results are completely irrelevant (advertisements for Naver services, PC sales, etc.). While the core relevant results are excellent, the presence of these irrelevant ads at the very top significantly increases the pollution level and requires filtering, reducing the overall immediate utility.
- **Comparison Summary:**
  > Query A ('당근마켓') demonstrates the search engine's strong understanding of the single entity, delivering extremely relevant, clean, and high-quality results with no pollution or morphological splitting. This provides an excellent foundation for an AI agent to gather general information about Danggeun Market. Query B ('당근 테크블로그') effectively uses the domain-anchored expansion to target a specific type of content (tech blog) related to the entity. The *organic* relevant results for Query B are excellent and highly specific to the user's intent. However, the overall quality and pollution level for Query B are negatively impacted by the presence of multiple irrelevant advertisements at the top of the results, which an AI agent would need to filter out. The query expansion successfully narrowed the intent, but the search engine's presentation of results included significant noise not present in the more general query.

---

### TC-NAV-03: 토스 (Toss - Fintech Service)
- **Query A (Original):** `토스`
- **Query B (Expanded):** `토스 테크블로그`
- **Scoring Breakdown:**
  - **Relevance:** Query A: `5/5` | Query B: `1/5`
  - **Pollution Level:** Query A: `5/5` | Query B: `1/5`
  - **Overall Quality:** Query A: `5/5` | Query B: `1/5`
- **Judge Analysis (Query A):**
  > The search results for '토스' are extremely relevant and directly target the 'Toss - Fintech Service' entity. All top 10 results are official links, including the main website, career page, company information, specific services (Toss Cert), customer support, app store link, and official social media/blog presences. There are no irrelevant results, advertisements, or morphological splitting errors. The snippets accurately describe the content and are highly informative.
- **Judge Analysis (Query B):**
  > The search results for '토스 테크블로그' are completely irrelevant and highly polluted. Every single result is an advertisement for other financial services, investment platforms ('모햇!'), or stock analysis tools, with no connection to 'Toss' or its 'tech blog'. This indicates a severe failure in query interpretation, where the search engine prioritized generic financial ads over the specific entity and intent. There are no morphological splitting errors of '토스' itself, but the query '토스 테크블로그' was entirely misinterpreted, leading to extreme commercial pollution.
- **Comparison Summary:**
  > Query A ('토스') provided excellent results, demonstrating a robust understanding of the single-noun entity and returning a clean, highly relevant set of official links for the Toss fintech service. In stark contrast, Query B ('토스 테크블로그'), which was an attempt at query expansion to find a more specific resource from Toss, failed completely. The search engine returned 100% irrelevant ads for other financial products, indicating a severe misinterpretation of the user's intent. The query expansion did not resolve any potential morphological splitting (which wasn't an issue for '토스' anyway) or improve quality; instead, it led to extreme pollution and zero utility. This highlights a critical limitation in Naver's ability to handle domain-anchored queries for specific sub-entities, particularly when 'ads' are heavily prioritized.

---

## 🏆 Final Conclusion & Recommendations

- **Average Original Quality (A):** `3.67/5`
- **Average Expanded Quality (B):** `3.00/5`
- **Quality Improvement Rate:** `-18.2%`

### Recommendations for Query Expansion Rules:
1. **Suspected Single Noun Entities**: Always enforce exact match quotes `"query"` or append domain-anchored context suffixes (e.g. `인프런`, `테크블로그`, `유튜브`) for single nouns that risk morphological splitting (e.g. `제로초` -> `제로` + `초`).
2. **Dynamic Expansion Rules**: Integrate into the agent's R-rules to detect single-noun inputs in Korean and automatically execute exact-quoted or suffixed queries if the initial search returns irrelevant/polluted results.
