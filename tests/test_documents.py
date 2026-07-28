from fastapi.testclient import TestClient
from app.main import app

def test_post_check(client):
    user=client.post("/api/v1/users", json={
        "email": "doctest@example.com",
        "username": "doctestuser",
        "password": "testpass123",
    })
    user_id=user.json()["id"]
    response= client.post(f"/api/v1/documents?user_id={user_id}",json={
        "title":"first doc",
        "content":"some content"
    })
    assert response.status_code==201
    assert response.json()["title"]=="first doc"
    assert response.json()["user_id"]==user_id

def test_get_documents_list(client):
    user = client.post("/api/v1/users", json={
        "email": "doc@example.com",
        "username": "doctuser",
        "password": "testpass123",
    })
    user_id = user.json()["id"]

    client.post(f"/api/v1/documents?user_id={user_id}", json={
        "title": "first doc",
        "content": "some content"
    })

    list_response = client.get(f"/api/v1/documents?user_id={user_id}")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["title"] == "first doc"

def test_get_documents_by_id(client):
    user = client.post("/api/v1/users", json={
        "email": "doc@example.com",
        "username": "doctuser",
        "password": "testpass123",
    })
    user_id = user.json()["id"]

    doc = client.post(f"/api/v1/documents?user_id={user_id}", json={
        "title": "first doc",
        "content": "some content"
    })
    document_id = doc.json()["id"]

    response = client.get(f"/api/v1/documents/{document_id}?user_id={user_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "first doc"

def test_get_document_not_found(client):
    response = client.get("/api/v1/documents/99999?user_id=1")
    assert response.status_code == 404


def test_update_document(client):
        user = client.post("/api/v1/users", json={
            "email": "doc@example.com",
            "username": "doctuser",
            "password": "testpass123",
        })
        user_id = user.json()["id"]
    
        doc = client.post(f"/api/v1/documents?user_id={user_id}", json={
            "title": "first doc",
            "content": "some content"
        })
        document_id = doc.json()["id"]

        response=client.put(f"/api/v1/documents/{document_id}?user_id={user_id}", json={
            "title": "updated first doc",
            "content": "updated some content"
        })
        assert response.status_code == 200

        updated = response.json()
        assert updated["title"] == "updated first doc"
        assert updated["content"] == "updated some content"

def test_delete_document(client):
        user = client.post("/api/v1/users", json={
            "email": "doc@example.com",
            "username": "doctuser",
            "password": "testpass123",
        })
        user_id = user.json()["id"]
    
        doc = client.post(f"/api/v1/documents?user_id={user_id}", json={
            "title": "first doc",
            "content": "some content"
        })
        document_id = doc.json()["id"]  

        response=client.delete(f"/api/v1/documents/{document_id}?user_id={user_id}")   
        assert response.status_code == 204   

        res=client.get(f"/api/v1/documents/{document_id}?user_id={user_id}")
        assert res.status_code == 404






def test_cannot_access_others_users_document(client):   
     user1 = client.post("/api/v1/users", json={
                 "email": "doc1@example.com",
                 "username": "doctuser1",
                 "password": "testpass123",
             })
     user2 = client.post("/api/v1/users", json={
                 "email": "doc2@example.com",
                 "username": "doctuser2",
                 "password": "testpass123",
             })
     
     user_id_A=user1.json()["id"]     
     user_id_B=user2.json()["id"]

     doc = client.post(f"/api/v1/documents?user_id={user_id_A}", json={
         "title": "user A's private doc",
         "content": "secret content"
     })
     document_id = doc.json()["id"]

     document=client.get(f"/api/v1/documents/{document_id}?user_id={user_id_B}")
     assert document.status_code==404