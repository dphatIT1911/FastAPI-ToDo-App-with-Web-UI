import uuid
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"email": unique_email, "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

def test_login_user(client: TestClient):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"email": "testlogin@example.com", "password": "password123"}
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testlogin@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testlogin@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
