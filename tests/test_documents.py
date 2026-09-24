from fastapi.testclient import TestClient
from app.main import app

def test_post_check(client, auth_headers):
    response = client.post("/api/v1/documents", json={
        "title": "first doc",
        "content": "some content"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["title"] == "first doc"

def test_get_documents_list(client, auth_headers):
    client.post("/api/v1/documents", json={
        "title": "first doc",
        "content": "some content"
    }, headers=auth_headers)

    list_response = client.get("/api/v1/documents", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["title"] == "first doc"


def test_get_documents_by_id(client, auth_headers):


    doc = client.post("/api/v1/documents", json={
        "title": "first doc",
        "content": "some content"
    }, headers=auth_headers)
    document_id = doc.json()["id"]

    response = client.get(f"/api/v1/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "first doc"

def test_get_document_not_found(client, auth_headers):
    response = client.get("/api/v1/documents/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_document(client, auth_headers):
    
        doc = client.post(f"/api/v1/documents", json={
            "title": "first doc",
            "content": "some content"
        }, headers=auth_headers)
        document_id = doc.json()["id"]

        response=client.put(f"/api/v1/documents/{document_id}", headers=auth_headers, json={
            "title": "updated first doc",
            "content": "updated some content"
        })
        assert response.status_code == 200

        updated = response.json()
        assert updated["title"] == "updated first doc"
        assert updated["content"] == "updated some content"

def test_delete_document(client, auth_headers):
    doc = client.post("/api/v1/documents", json={
        "title": "first doc",
        "content": "some content"
    }, headers=auth_headers)
    document_id = doc.json()["id"]

    response = client.delete(f"/api/v1/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 204

    res = client.get(f"/api/v1/documents/{document_id}", headers=auth_headers)
    assert res.status_code == 404




def test_cannot_access_others_users_document(client, auth_headers):
    # auth_headers = user A's headers, already given to us

    # Step 1: create a document as user A
    doc = client.post("/api/v1/documents", json={
        "title": "user A's private doc",
        "content": "secret content"
    }, headers=auth_headers)
    document_id = doc.json()["id"]

    # Step 2: manually create + log in a SECOND user (user B) — auth_headers can't give us this
    client.post("/api/v1/users", json={
        "email": "userB@example.com",
        "username": "userB",
        "password": "testpass123",
    })
    login_b = client.post("/api/v1/auth/login", json={
        "email": "userB@example.com",
        "password": "testpass123",
    })
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    # Step 3: try to access user A's document AS user B
    response = client.get(f"/api/v1/documents/{document_id}", headers=headers_b)
    assert response.status_code == 404