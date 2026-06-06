import httpx
from bs4 import BeautifulSoup

async def google_search(query):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            "http://localhost:8080/search",
            params={
                "q": query
            },
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        articles = soup.select("article.result")

        for i, article in enumerate(articles[:10]):

            title_element = article.select_one("h3 a")

            if not title_element:
                continue

            title = title_element.get_text(
                separator=" ",
                strip=True
                )

            url = title_element.get("href", "")

            snippet_element = article.select_one(".content")

            snippet = ""

            if snippet_element:
                snippet = snippet_element.get_text(
                    
                    strip=True
                )

            results.append({
                "position": i + 1,
                "title": title,
                "url": url,
                "snippet": snippet
            })

        return results