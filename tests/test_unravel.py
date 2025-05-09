from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_unravel_valid_nested_json():
    payload = {
        "key1": {"keyA": ["foo", 0, "bar"]},
        "some other key": 2,
        "finally": "end",
    }
    response = client.post("/unravel", json=payload)
    assert response.status_code == 200
    assert response.json() == [
        "key1",
        "keyA",
        "foo",
        0,
        "bar",
        "some other key",
        2,
        "finally",
        "end",
    ]


def test_unravel_invalid_json():
    response = client.post("/unravel", content="not a json")
    assert response.status_code == 400
    assert "error" in response.json()


def test_unravel_non_object_json():
    # List instead of dict
    payload = ["a", "b", "c"]
    response = client.post("/unravel", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "Request payload must be a JSON object."


def test_unravel_at_max_depth():
    payload = nested = {}
    for i in range(9):
        nested[f"level_{i}"] = {}
        nested = nested[f"level_{i}"]
    nested["final"] = "value"

    response = client.post("/unravel", json=payload)
    assert response.status_code == 200
    assert "final" in response.json()


def test_unravel_exceeds_max_depth():
    payload = nested = {}
    for i in range(10):  # One level beyond the max
        nested[f"level_{i}"] = {}
        nested = nested[f"level_{i}"]
    nested["too_deep"] = "value"

    response = client.post("/unravel", json=payload)
    assert response.status_code == 400
    assert "Maximum recursion" in response.json()["error"]
