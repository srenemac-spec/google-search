from app.search import parse_search_results


def test_parse_search_results_returns_ten_valid_items():
    html = ["<html><body>"]
    for i in range(12):
        if i == 3:
            html.append(
                "<article class='result'><div class='content'>No title here</div></article>"
            )
            continue
        html.append(
            f"<article class='result'><h3><a href='http://example.com/{i}'>Title {i}</a></h3>"
            f"<div class='content'>Snippet {i}</div></article>"
        )
    html.append("</body></html>")
    html_content = "".join(html)

    results = parse_search_results(html_content)

    assert len(results) == 10
    assert results[0]["title"] == "Title 0"
    assert results[3]["title"] == "Title 4"
    assert results[-1]["title"] == "Title 10"
    assert [result["position"] for result in results] == list(range(1, 11))
