from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.api.routes.perform_roll_restart")
def test_roll_returns_202_on_merge_commit(mock_restart):
    payload = {
        "ref": "refs/heads/main",
        "head_commit": {"parents": ["abc123", "def456"]},
    }

    response = client.post(
        "/roll",
        headers={"X-GitHub-Event": "push"},
        json=payload,
    )

    assert response.status_code == 202
    assert response.json() == {"message": "Rolling update triggered"}
