from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)


@patch("app.main.google_search", new_callable=AsyncMock)
def test_search_response(mock_search):

    mock_search.return_value = [
        {
            "title": "Dog",
            "url": "https://example.com",
            "snippet": "A dog result"
        }
    ]

    response = client.post(
        "/search",
        json={"query": "dog"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "query" in data
    assert "results" in data
    assert isinstance(data["results"], list)


@patch("app.main.google_search", new_callable=AsyncMock)
def test_first_result_shape(mock_search):

    mock_search.return_value = [
        {
            "title": "Dog",
            "url": "https://example.com",
            "snippet": "A dog result"
        }
    ]

    response = client.post(
        "/search",
        json={"query": "dog"}
    )

    result = response.json()["results"][0]

    assert "title" in result
    assert "url" in result
    assert "snippet" in result
