import httpx
from bs4 import BeautifulSoup
import os

SEARXNG_URL = os.getenv(
    "SEARXNG_URL",
    "http://localhost:8080"
)


def _extract_search_result(article):
    title_element = (
        article.select_one("h3 a")
        or article.select_one("h2 a")
        or article.select_one(".result__title a")
        or article.select_one("a[href]")
    )
    if not title_element:
        return None

    url = title_element.get("href", "").strip()
    if not url:
        return None

    snippet_element = article.select_one(
        ".content, .result__snippet, .result__description, .description"
    )
    snippet = snippet_element.get_text(strip=True) if snippet_element else ""

    return {
        "title": title_element.get_text(separator=" ", strip=True),
        "url": url,
        "snippet": snippet,
    }


def parse_search_results(html, max_results=10):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen_urls = set()

    for article in soup.select("article.result"):
        result = _extract_search_result(article)
        if not result:
            continue
        
        if result["url"] in seen_urls:
            continue

        seen_urls.add(result["url"])
        results.append({"position": len(results) + 1, **result})

        if len(results) >= max_results:
            break

    return results


async def _fetch_search_page(query, page=None):
    params = {"q": query}

    if page is not None:
        params["pageno"] = page

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=60,
        )

    return response.text

    

async def google_search(query, max_results=10, max_pages=5):
    results = []
    seen_urls = set()
    page = 1

    while len(results) < max_results and page <= max_pages:
        remaining = max_results - len(results)
        html = await _fetch_search_page(query, page=page)
        page_results = parse_search_results(html, max_results=remaining)

        for result in page_results:
            if result["url"] in seen_urls:
                continue
            seen_urls.add(result["url"])
            results.append({**result, "position": len(results) + 1})
            if len(results) >= max_results:
                break

        if len(results) >= max_results:
            break

        if len(page_results) == 0:
            break

        page += 1

    return results[:max_results]
