import asyncio

from app import search


async def fake_fetch_page(query, page=None):
    pages = {
        1: "<html><body>"
           "<article class='result'><h3><a href='http://example.com/1'>Title 1</a></h3>"
           "<div class='content'>Snippet 1</div></article>"
           "<article class='result'><h3><a href='http://example.com/2'>Title 2</a></h3>"
           "<div class='content'>Snippet 2</div></article>"
           "</body></html>",
        2: "<html><body>"
           "<article class='result'><h3><a href='http://example.com/3'>Title 3</a></h3>"
           "<div class='content'>Snippet 3</div></article>"
           "<article class='result'><h3><a href='http://example.com/4'>Title 4</a></h3>"
           "<div class='content'>Snippet 4</div></article>"
           "</body></html>",
    }
    return pages.get(page, "<html><body></body></html>")


def test_google_search_min_results():
    original_fetch = search._fetch_search_page
    search._fetch_search_page = fake_fetch_page

    try:
        results = asyncio.run(search.google_search("dog", max_results=4, min_results=4, max_pages=2))
        assert len(results) == 4
        assert [r["title"] for r in results] == [
            "Title 1",
            "Title 2",
            "Title 3",
            "Title 4",
        ]
    finally:
        search._fetch_search_page = original_fetch


def test_google_search_positions_are_sequential_across_pages():
    original_fetch = search._fetch_search_page
    search._fetch_search_page = fake_fetch_page

    try:
        results = asyncio.run(search.google_search("dog", max_results=4, min_results=4, max_pages=2))
        assert [result["position"] for result in results] == [1, 2, 3, 4]
        assert [result["title"] for result in results] == [
            "Title 1",
            "Title 2",
            "Title 3",
            "Title 4",
        ]
    finally:
        search._fetch_search_page = original_fetch


def test_google_search_min_results_validates_arguments():
    try:
        asyncio.run(search.google_search("dog", max_results=3, min_results=4))
        assert False, "Expected ValueError when min_results > max_results"
    except ValueError as exc:
        assert "min_results cannot be greater than max_results" in str(exc)
