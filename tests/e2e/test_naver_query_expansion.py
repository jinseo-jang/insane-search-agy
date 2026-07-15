#!/usr/bin/env python3
"""
E2E Test Script for Naver Query Expansion Verification using Agent-as-Judge.
Executes queries, extracts results, calls Gemini to evaluate them,
and generates the comparative evaluation report.
"""

import os
import sys
import json
import time
import urllib.parse
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# Setup path to locate engine
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "skills", "insane-search"))

try:
    from engine import fetch
except ImportError:
    print("Error: Could not import engine. Ensure PYTHONPATH includes skills/insane-search")
    sys.exit(1)

TEST_CASES = [
    {
        "id": "TC-NAV-01",
        "entity": "제로초 (ZeroCho - Blogger/Developer)",
        "query_a": "제로초",
        "query_b": "제로초 인프런",
    },
    {
        "id": "TC-NAV-02",
        "entity": "당근마켓 (Danggeun Market - Local Marketplace)",
        "query_a": "당근마켓",
        "query_b": "당근 테크블로그",
    },
    {
        "id": "TC-NAV-03",
        "entity": "토스 (Toss - Fintech Service)",
        "query_a": "토스",
        "query_b": "토스 테크블로그",
    }
]

def is_descendant_of_a(node):
    p = node.parent
    while p:
        if p.name == "a":
            return True
        p = p.parent
    return False

def extract_search_results(html: str) -> list[dict]:
    """Extract top search titles and snippets from Naver Search HTML using robust selector-free heuristic."""
    soup = BeautifulSoup(html, "html.parser")
    main_pack = soup.select_one("#main_pack")
    if not main_pack:
        return []
        
    links = main_pack.find_all("a")
    grouped_results = {}
    
    for link in links:
        href = link.get("href", "")
        if not href:
            continue
        
        # Only keep http/https links
        if not (href.startswith("http://") or href.startswith("https://")):
            continue
            
        # Filter out obvious internal/navigation URLs
        if "search.naver" in href or "nid.naver.com" in href or "help.naver.com" in href:
            continue
        if "policy.naver.com" in href or "cr.naver.com" in href or "keep.naver.com" in href:
            continue
        if "share.naver.com" in href or "me.naver.com" in href:
            continue
            
        text = link.get_text(strip=True)
        # Clean up common helper texts
        for noise in ("새 창 열림", "Keep에 바로가기", "동영상 바로재생", "Keep 저장", "바로가기", "공유하기"):
            text = text.replace(noise, "")
        text = text.strip()
        
        if len(text) < 2:
            continue
            
        if href not in grouped_results:
            grouped_results[href] = {
                "texts": set(),
                "link_element": link
            }
        grouped_results[href]["texts"].add(text)
        
    extracted_results = []
    for href, info in grouped_results.items():
        sorted_texts = sorted(list(info["texts"]), key=len, reverse=True)
        title = sorted_texts[0]
        
        link_el = info["link_element"]
        snippet = ""
        p = link_el.parent
        for depth in range(4):
            if not p or p.name in ("body", "html"):
                break
                
            import copy
            p_copy = copy.copy(p)
            for s in p_copy.find_all(["script", "style"]):
                s.decompose()
                
            text_nodes = []
            for el in p_copy.find_all(string=True):
                if not is_descendant_of_a(el):
                    txt = el.strip()
                    if txt and len(txt) > 20:
                        text_nodes.append(txt)
            if text_nodes:
                snippet = " ".join(text_nodes)
                snippet = " ".join(snippet.split())
                if snippet:
                    break
                    
            fallback_texts = []
            for el in p_copy.find_all(string=True):
                txt = el.strip()
                if txt and len(txt) > 20 and txt != title:
                    fallback_texts.append(txt)
            if fallback_texts:
                snippet = " ".join(fallback_texts)
                snippet = " ".join(snippet.split())
                if snippet:
                    break
                    
            p = p.parent
            
        extracted_results.append({
            "title": title,
            "snippet": snippet,
            "link": href
        })
        
    deduped_results = []
    seen_titles = set()
    for r in extracted_results:
        t_lower = r["title"].lower()
        if t_lower not in seen_titles:
            seen_titles.add(t_lower)
            deduped_results.append(r)
            
    return deduped_results[:10]

def run_naver_search(query: str) -> str:
    """Fetch search page content via the insane-search engine."""
    url = f"https://search.naver.com/search.naver?query={urllib.parse.quote(query)}"
    # Fix from explorer_2: success_selectors=["#main_pack", "#container", "#wrap"]
    res = fetch(url, enable_playwright=True, success_selectors=["#main_pack", "#container", "#wrap"])
    if not res.ok:
        raise RuntimeError(f"Engine failed to fetch search results for query '{query}': {res.summary}")
    return res.content

def judge_comparison(client: genai.Client, case_id: str, entity: str, query_a: str, results_a: list, query_b: str, results_b: list) -> dict:
    """Invoke Gemini API to evaluate and compare search result quality."""
    
    prompt = f"""You are an expert Search Quality Evaluator. Your task is to perform a comparative evaluation of search results retrieved from Naver Search for two versions of a search query targetting the entity: "{entity}".

1. Query A (Original single-noun query): "{query_a}"
2. Query B (Expanded domain-anchored query): "{query_b}"

You will analyze the search results (titles and snippets) for both queries and grade them on three metrics: Relevance, Pollution Level, and Overall Quality.

### Metrics Definitions

1. Relevance (1-5):
   - Measure how well the search results match the user's core intended entity/concept "{entity}".
   - Results about unrelated concepts (e.g. general dictionary definitions, unrelated companies, words split incorrectly) are irrelevant.
   - 5: Extremely relevant. All top results target "{entity}".
   - 3: Moderately relevant. About half of the results are irrelevant or drift.
   - 1: Completely irrelevant. All results drift.

2. Pollution Level (1-5):
   - Measure the presence of noise, spam, advertisements, or morphological splitting errors.
   - Morphological splitting error: The search engine splits a single noun query (e.g., "제로초" -> "제로" + "초"; "당근마켓" -> "당근" + "마켓") and matches them independently, leading to completely unrelated results (e.g., carrot recipes for "당근마켓", zero sugar for "제로초").
   - 5: Very Low Pollution. No splitting errors, ads, or spam.
   - 3: Medium Pollution. 2-3 results exhibit splitting errors or irrelevant ads.
   - 1: Extreme Pollution. All results exhibit splitting errors or irrelevant ads.

3. Overall Quality (1-5):
   - A holistic score representing the utility of the search results for an AI agent to answer questions about the target entity "{entity}".
   - 5: Excellent. Highly informative and clean.
   - 3: Fair. Informative but requires heavy filtering of noise.
   - 1: Unusable. No useful information about the target entity.

### Search Results Data

Query A: "{query_a}"
Results:
{json.dumps(results_a, ensure_ascii=False, indent=2)}

Query B: "{query_b}"
Results:
{json.dumps(results_b, ensure_ascii=False, indent=2)}

### Output Format
Provide your comparative evaluation in raw JSON format (no markdown blocks, just the JSON object itself) containing:
{{
  "query_a": {{
    "relevance": <int>,
    "pollution_level": <int>,
    "overall_quality": <int>,
    "analysis": "<Detailed qualitative analysis of results for Query A, pointing out morphological splitting or drift if any>"
  }},
  "query_b": {{
    "relevance": <int>,
    "pollution_level": <int>,
    "overall_quality": <int>,
    "analysis": "<Detailed qualitative analysis of results for Query B, pointing out improvements or issues>"
  }},
  "comparison_summary": "<Synthesis comparing Query A vs Query B, highlighting if the query expansion successfully resolved morphological splitting, reduced pollution, and improved quality>"
}}
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing JSON from judge response: {e}\nRaw response: {response.text}")
        return {
            "query_a": {"relevance": 1, "pollution_level": 1, "overall_quality": 1, "analysis": "Failed to parse judge output"},
            "query_b": {"relevance": 1, "pollution_level": 1, "overall_quality": 1, "analysis": "Failed to parse judge output"},
            "comparison_summary": f"Error parsing judge output: {e}"
        }

def main():
    print("Initializing Agent-as-Judge Client...")
    client = genai.Client(vertexai=True)
    
    report_file = os.path.join(ROOT, "tests", "e2e", "naver_query_expansion_eval.md")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    eval_results = []
    
    for tc in TEST_CASES:
        print(f"\nEvaluating Case {tc['id']}: {tc['entity']}")
        
        # 1. Run Query A (Original)
        print(f"  Fetching Query A: '{tc['query_a']}'...")
        html_a = run_naver_search(tc["query_a"])
        results_a = extract_search_results(html_a)
        print(f"    Extracted {len(results_a)} results.")
        
        # 2. Run Query B (Expanded - Domain-Anchored)
        chosen_query_b = tc["query_b"]
        print(f"  Fetching Query B: '{chosen_query_b}'...")
        html_b = run_naver_search(chosen_query_b)
        results_b = extract_search_results(html_b)
        print(f"    Extracted {len(results_b)} results.")
        
        # 3. Judge the pair
        print("  Calling Agent-as-Judge...")
        evaluation = judge_comparison(
            client=client,
            case_id=tc["id"],
            entity=tc["entity"],
            query_a=tc["query_a"],
            results_a=results_a,
            query_b=chosen_query_b,
            results_b=results_b
        )
        
        eval_results.append({
            "id": tc["id"],
            "entity": tc["entity"],
            "query_a": tc["query_a"],
            "query_b": chosen_query_b,
            "evaluation": evaluation
        })
        
        print(f"    Scores (A vs B):")
        print(f"      Relevance:       {evaluation['query_a']['relevance']} -> {evaluation['query_b']['relevance']}")
        print(f"      Pollution Level: {evaluation['query_a']['pollution_level']} -> {evaluation['query_b']['pollution_level']}")
        print(f"      Overall Quality: {evaluation['query_a']['overall_quality']} -> {evaluation['query_b']['overall_quality']}")

    # 4. Generate Comparative Evaluation Report
    date_str = time.strftime('%Y-%m-%d')
    
    print(f"\nWriting evaluation report to {report_file}...")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Naver Search Query Expansion Comparative Evaluation Report\n\n")
        f.write(f"**Status:** Completed & Evaluated  \n")
        f.write(f"**Evaluator:** Agent-as-Judge (model: `gemini-2.5-flash` via Vertex AI)  \n")
        f.write(f"**Date:** {date_str}  \n")
        f.write(f"**Test Suite:** Naver Search Query Expansion Verification  \n\n")
        f.write("---\n\n")
        
        f.write("## 📊 Summary of Evaluation Metrics\n\n")
        f.write("| Test Case | Query A (Original) | Query B (Expanded) | Relevance (A / B) | Pollution Level (A / B) | Overall Quality (A / B) | Status |\n")
        f.write("|---|---|---|:---:|:---:|:---:|:---:|\n")
        
        for r in eval_results:
            eva = r["evaluation"]
            # A test passes if quality is improved or maintained high (e.g. B overall quality >= 3 and >= A quality)
            pass_status = "PASS ✅" if eva["query_b"]["overall_quality"] >= 4 and eva["query_b"]["overall_quality"] >= eva["query_a"]["overall_quality"] else "FAIL ❌"
            f.write(f"| **{r['id']}** | `{r['query_a']}` | `{r['query_b']}` | {eva['query_a']['relevance']} / {eva['query_b']['relevance']} | {eva['query_a']['pollution_level']} / {eva['query_b']['pollution_level']} | {eva['query_a']['overall_quality']} / {eva['query_b']['overall_quality']} | **{pass_status}** |\n")
        
        f.write("\n*Note: Relevance and Overall Quality scores are 1-5 (higher is better). Pollution Level is 1-5 (higher means LESS pollution, i.e., cleaner).*  \n")
        f.write("*Pass Status definition: Query B overall quality must be >= 4 and >= Query A overall quality.*\n\n")
        f.write("---\n\n")
        
        f.write("## 💯 Detailed Evaluation per Test Case\n\n")
        for r in eval_results:
            eva = r["evaluation"]
            f.write(f"### {r['id']}: {r['entity']}\n")
            f.write(f"- **Query A (Original):** `{r['query_a']}`\n")
            f.write(f"- **Query B (Expanded):** `{r['query_b']}`\n")
            f.write("- **Scoring Breakdown:**\n")
            f.write(f"  - **Relevance:** Query A: `{eva['query_a']['relevance']}/5` | Query B: `{eva['query_b']['relevance']}/5`\n")
            f.write(f"  - **Pollution Level:** Query A: `{eva['query_a']['pollution_level']}/5` | Query B: `{eva['query_b']['pollution_level']}/5`\n")
            f.write(f"  - **Overall Quality:** Query A: `{eva['query_a']['overall_quality']}/5` | Query B: `{eva['query_b']['overall_quality']}/5`\n")
            f.write("- **Judge Analysis (Query A):**\n")
            f.write(f"  > {eva['query_a']['analysis']}\n")
            f.write("- **Judge Analysis (Query B):**\n")
            f.write(f"  > {eva['query_b']['analysis']}\n")
            f.write("- **Comparison Summary:**\n")
            f.write(f"  > {eva['comparison_summary']}\n\n")
            f.write("---\n\n")
            
        # Overall Summary stats
        avg_quality_a = sum(r["evaluation"]["query_a"]["overall_quality"] for r in eval_results) / len(eval_results)
        avg_quality_b = sum(r["evaluation"]["query_b"]["overall_quality"] for r in eval_results) / len(eval_results)
        f.write("## 🏆 Final Conclusion & Recommendations\n\n")
        f.write(f"- **Average Original Quality (A):** `{avg_quality_a:.2f}/5`\n")
        f.write(f"- **Average Expanded Quality (B):** `{avg_quality_b:.2f}/5`\n")
        improvement = ((avg_quality_b - avg_quality_a) / avg_quality_a * 100) if avg_quality_a > 0 else 0
        f.write(f"- **Quality Improvement Rate:** `{improvement:.1f}%`\n\n")
        f.write("### Recommendations for Query Expansion Rules:\n")
        f.write("1. **Suspected Single Noun Entities**: Always enforce exact match quotes `\"query\"` or append domain-anchored context suffixes (e.g. `인프런`, `테크블로그`, `유튜브`) for single nouns that risk morphological splitting (e.g. `제로초` -> `제로` + `초`).\n")
        f.write("2. **Dynamic Expansion Rules**: Integrate into the agent's R-rules to detect single-noun inputs in Korean and automatically execute exact-quoted or suffixed queries if the initial search returns irrelevant/polluted results.\n")

    print("Comparative evaluation report generated successfully.")

if __name__ == "__main__":
    main()
