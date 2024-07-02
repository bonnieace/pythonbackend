# app/tests/test_summary.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_summary():
    response = client.get("/summary")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
