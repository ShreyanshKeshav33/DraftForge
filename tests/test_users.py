from fastapi.testclient import TestClient
from app.main import app



def test_post_check(client):
    response= client.post("/api/v1/users", json={
        "email":"test2@example.com",
        "username":"test2user",
        "password":"testpass123",

    })
    assert response.status_code == 201
    assert response.json()["email"]=="test2@example.com"
    assert response.json()["username"]=="test2user"

def test_create_duplicate_user(client):
    client.post("/api/v1/users", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    })
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    })
    assert response.status_code == 400

def test_get_user_by_id(client):
    create = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    })
    user_id = create.json()["id"]
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404

def test_delete_user(client):
    create = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    })
    user_id = create.json()["id"]
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

def test_delete_user_not_found(client):
    response = client.delete("/api/v1/users/9999")
    assert response.status_code == 404

   


