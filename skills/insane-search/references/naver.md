# 네이버 계열 접근 전략

> 네이버 서비스별로 접근 방법이 다르다. 블로그는 모바일 URL, 뉴스/증권은 Jina Reader.

## 네이버 블로그

WebFetch 차단. 모바일 URL 변환 + iPhone UA로 접근.

```bash
# blog.naver.com/{ID}/{NO} → m.blog.naver.com 변환
curl -sL \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
  -H "Accept-Language: ko-KR,ko;q=0.9" \
  -H "Referer: https://m.naver.com/" \
  "https://m.blog.naver.com/PostView.naver?blogId={ID}&logNo={NO}"
```

RSS도 가능 (최신 50개, 본문 약 300자):
```bash
curl -sL "https://rss.blog.naver.com/{BLOG_ID}.xml"
```

## 네이버 뉴스

Jina Reader로 완전 접근 가능.

```bash
# 기사 목록
curl -s "https://r.jina.ai/https://news.naver.com/"

# 개별 기사
curl -s "https://r.jina.ai/https://n.news.naver.com/article/{press_id}/{article_id}"
```

## 네이버 증권

Jina Reader로 실시간 주가, 주요 뉴스 접근.

```bash
curl -s "https://r.jina.ai/https://finance.naver.com/item/main.naver?code={종목코드}"
```

## 네이버 금융 시세 (비공식, 무인증)

인증 불필요. 주가 시계열 데이터 JSON 반환.

```bash
# 일봉 시세 (삼성전자=005930)
curl -sL "https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20240101&endTime=20241231&timeframe=day"

# 분봉
curl -sL "https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=0&timeframe=minute&count=200"
```

응답: `[[날짜, 시가, 고가, 저가, 종가, 거래량, 외국인거래율], ...]`

## 네이버 검색 (신원위장으로 직접 접근)

curl_cffi + 세션 쿠키 워밍으로 네이버 검색 결과를 직접 크롤링할 수 있다. API 키 불필요.

```python
from curl_cffi import requests
from urllib.parse import quote

s = requests.Session(impersonate="chrome124")
s.headers.update({
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.google.com/",
})
s.get("https://www.naver.com/", timeout=10)  # 쿠키 워밍
s.headers["Referer"] = "https://www.naver.com/"

# 통합 검색 (블로그+뉴스+웹 혼합)
r = s.get(f"https://search.naver.com/search.naver?query={quote('검색어')}")

# 블로그 탭
r = s.get(f"https://search.naver.com/search.naver?where=post&query={quote('검색어')}")

# 뉴스 탭
r = s.get(f"https://search.naver.com/search.naver?where=news&query={quote('검색어')}")
```

### 추출 가능한 데이터

| 탭 | URL 패턴 | 추출 |
|---|---|---|
| 통합 | `search.naver?query=` | 블로그 URL, 외부 링크, 뉴스 |
| 블로그 | `where=post&query=` | blog.naver.com URL, 제목, 스니펫 |
| 뉴스 | `where=news&query=` | n.news.naver.com URL, 제목 |

### 한국어 키워드 검색의 핵심 경로

WebSearch는 한국어 신규 콘텐츠 인덱싱이 지연되지만, 네이버 검색은 한국어에 최적화되어 있다.
**한국 사이트 키워드 검색 → 네이버 검색 직접 접근이 가장 정확하고 빠르다.**

### 형태소 분할(Morphological Splitting) 문제 및 해결 방안

네이버 검색은 한국어 형태소 분석을 기반으로 작동하므로, 등록되지 않은 단일 명사(신생 브랜드, 인명, 서비스명 등)에 대해 형태소 분할(Splitting) 및 이로 인한 검색 결과 오염(Pollution)이 빈번하게 발생합니다.

#### 1. 문제 메커니즘
1. **형태소 토큰화**: 네이버 사전이나 사전 구축된 고유명사 사전에 단어가 등록되어 있지 않으면 형태소 분석기가 이를 분절합니다 (예: `제로초` -> `제로` + `초`, `당근마켓` -> `당근` + `마켓`).
2. **결과 백필링 (Backfilling)**: 해당 단일 키워드와 완벽하게 매칭되는 문서 수가 적을 경우, 분절된 개별 형태소(`제로`, `당근` 등)를 포함하는 고권위 문서(예: 제로 콜라, 공기청정기 제로, 당근 요리법 등)로 검색 결과 리스트를 무리하게 채우며, HTML 상에서 이들 개별 단어를 `<mark>` 태그로 강조 표시합니다.
3. **결과 오염**: 이로 인해 검색 결과 목록에 불필요한 노이즈가 급증하여 AI 에이전트의 검색 정확도가 하락합니다.

#### 2. 접미사 완화 매트릭스 (Suffix Mitigation Matrix) 및 광고 오염 트레이드오프 (Ad-Pollution Trade-off)
검색어의 형태소 분할 및 컨텍스트 이탈을 제어하기 위해, 특정 상황에서는 단순 `블로그`, `공식 홈페이지` 같은 범용 접미사 대신 **도메인 앵커링이 강력한 특정 접미사**를 함께 조합하여 2차 검색을 수행해야 합니다.

| 대상 엔티티 유형 | 단일 명사 예시 | 추천 도메인 앵커링 접미사 (Query B) | 접미사 선정 이유 및 메커니즘 | 피해야 할 범용 접미사 (오염 촉진) |
| :--- | :--- | :--- | :--- | :--- |
| **개인 / 개발자 / 강사** | `제로초`, `생활코딩` | `인프런`, `유튜브`, `깃허브`, `강의`, `자바스크립트` | 기술 교육 및 소스코드 저장소 맥락으로 고정하여 형태소 분리 방지 | `블로그`, `공식`, `홈페이지` (예: `제로` + `블로그` 분할로 공기청정기, 정수기 노출) |
| **IT 스타트업 / 기업** | `토스`, `당근마켓` | `테크블로그`, `채용`, `기술블로그`, `팀` | 기업 프로필 및 기술 공유 맥락을 강제하여 동음이의어 방지 | `블로그` (예: 하나 트래블로그 카드 등 타사 상품 노출 오염) |
| **일반 브랜드 / 서비스** | `토스` | `금융`, `송금`, `계좌` | 주 비즈니스 도메인 키워드를 함께 매칭하여 문맥 필터링 수행 | `공식` (너무 광범위하여 다른 분야의 공식 매칭) |

⚠️ **광고 오염 트레이드오프 (Ad-Pollution Trade-off)**
이미 널리 알려진 기성 브랜드나 대기업(예: `토스`, `당근마켓`)의 경우, 단일 키워드로 검색해도 형태소 분할이나 컨텍스트 이탈 없이 깨끗하고 정확한 공식 검색 결과가 상위에 노출됩니다.
이러한 인지도 높은 키워드에 대해 성급하게 쿼리 확장(예: `토스 테크블로그`)을 적용하면, 네이버의 파워링크 광고가 최상단에 대량 노출(예: 8개 이상)되면서 실제 검색 대상(예: `toss.tech`)이 9~10위 이하로 완전히 밀려나는 역효과(광고 오염)가 발생하여 검색 품질이 현저히 나빠집니다.

따라서 쿼리 확장은 무조건 적용하는 것이 아니며, **선택적·조건부 fallback/remediation 전략**으로 사용해야 합니다:
1. **단일 키워드 검색 시 심각한 형태소 분할이나 결과 오염이 발생하는 경우** (예: 인지도가 낮은 고유명사인 `제로초` 검색 시 `제로` + `초`로 분리되어 엉뚱한 결과가 백필링되는 경우).
2. **최초 단일 검색 시도 후, 결과 리스트의 품질이 낮거나 원하는 정보를 확보하지 못한 경우**.

#### 3. 모범 사례 분석 (Best-Practice Examples)
* **사례 A**: `제로초` 검색
  * **단일 검색 (`제로초`)**: 검색 노출 수 제한 및 "제로"가 포함된 공기청정기 등이 백필링됨.
  * **나쁜 확장 (`제로초 블로그`)**: "제로" + "블로그" 분할 매칭으로 인해 방탈출 카페, 정수기 광고로 도배됨 (오염 극대화).
  * **좋은 확장 (`제로초 인프런`)**: IT 기술 교육 플랫폼과 매칭되어 강사 소개 및 강의 목록 100% 매칭 성공.
* **사례 B**: `토스` 검색
  * **단일 검색 (`토스`)**: 공식 홈페이지(`toss.im`), 채용, 고객센터 등 유용한 정보가 상위에 오염 없이 100% 매칭됨 (최적의 품질).
  * **잘못된 확장 (`토스 테크블로그`)**: 토스 공식 기술 블로그(`toss.tech`)가 최상위에 정밀 매칭되는 것이 아니라, 8개의 파워링크 광고에 밀려 검색 결과 9위/10위로 전락하여 결과 품질이 심각하게 저하됨 (광고 오염 발생).


## 네이버 카페

로그인 + iframe 이중 장벽. 본문 직접 접근 불가.
fallback 체인에서 Phase 1~3을 시도하되, login/paywall 감지 시 "인증 필요"로 종료.

## 네이버 TV

yt-dlp로 접근 (media.md 참조).

```bash
yt-dlp --dump-json "https://tv.naver.com/v/{video_id}"
```
