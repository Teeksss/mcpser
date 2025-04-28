from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_user_list_unauthorized():
    r = client.get("/api/v1/users/")
    assert r.status_code == 401 or r.status_code == 403

def test_register_and_login():
    data = {"username": "testuser", "password": "testpass", "email": "test@example.com"}
    r = client.post("/api/v1/auth/register", json=data)
    assert r.status_code == 200 or r.status_code == 409
    r = client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass"})
    assert r.status_code == 200
    assert "access_token" in r.json()