from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_search_response():

    response = client.post(
        "/search",
        json={
            "query": "dog"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "query" in data
    assert "results" in data

    assert isinstance(
        data["results"],
        list
    )

def test_first_result_shape():

    response = client.post(
        "/search",
        json={
            "query": "dog"
        }
    )

    result = response.json()[
        "results"
    ][0]

    assert "title" in result
    assert "url" in result
    assert "snippet" in result