from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello_world_plain_text():
    response = client.get("/helloworld")
    assert response.status_code == 200
    assert response.text == "Hello World!"
    assert response.headers["content-type"].startswith("text/plain")


def test_hello_world_json():
    response = client.get("/helloworld", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
    assert response.headers["content-type"].startswith("application/json")


def test_hello_world_with_compound_accept_header():
    headers = {"Accept": "application/json, text/html;q=0.9"}
    response = client.get("/helloworld", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
    assert response.headers["content-type"].startswith("application/json")


def test_helloworld_plain_with_valid_tz():
    response = client.get("/helloworld?tz=Europe/London")
    assert response.status_code == 200
    assert "Hello World! It is" in response.text
    assert "Europe/London" in response.text


def test_helloworld_json_with_valid_tz():
    response = client.get(
        "/helloworld?tz=America/New_York", headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Hello World! It is" in data["message"]
    assert "America/New_York" in data["message"]


def test_helloworld_with_invalid_tz():
    response = client.get("/helloworld?tz=NotARealZone")
    assert response.status_code == 400
    assert response.json()["error"].startswith("Invalid timezone")


def test_helloworld_with_compound_accept_and_valid_tz():
    response = client.get(
        "/helloworld?tz=Asia/Tokyo", headers={"Accept": "application/json, text/html"}
    )
    assert response.status_code == 200
    assert "Asia/Tokyo" in response.json()["message"]
