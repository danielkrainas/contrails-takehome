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
