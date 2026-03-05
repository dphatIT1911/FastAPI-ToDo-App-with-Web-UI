import uuid
from fastapi.testclient import TestClient

def get_token(client: TestClient) -> str:
    # Register and login generic test user with unique email
    unique_email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    client.post("/api/v1/auth/register", json={"email": unique_email, "password": "password123"})
    res = client.post("/api/v1/auth/login", data={"username": unique_email, "password": "password123"})
    return res.json().get("access_token", "")

def test_auth_fail(client: TestClient):
    response = client.get("/api/v1/todos")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_validation_fail(client: TestClient):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Title less than 3 chars should fail
    response = client.post("/api/v1/todos", json={"title": "ab"}, headers=headers)
    assert response.status_code == 422

def test_create_success(client: TestClient):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create valid todo
    payload = {
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs",
        "tags": ["shopping"]
    }
    response = client.post("/api/v1/todos", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Buy groceries"
    assert "shopping" in response.json()["tags"]

def test_get_404(client: TestClient):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting a non-existent todo ID
    response = client.get("/api/v1/todos/99999", headers=headers)
    assert response.status_code == 404
