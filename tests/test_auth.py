import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_ping():
    r = client.get("/api/v1/ping")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}