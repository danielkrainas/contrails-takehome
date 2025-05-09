from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.api.routes.perform_roll_restart")
def test_roll_returns_202(mock_restart):
    response = client.post("/roll")
    assert response.status_code == 202
    assert response.json() == {"message": "Rolling update triggered"}
