# app/tests/test_entries.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_entry():
    response = client.post("/entries", json={"title": "Test Entry", "content": "This is a test"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Entry"

def test_read_entries():
    response = client.get("/entries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
