from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == settings.app_version
    assert response.json()["debug"] == settings.debug

def test_settings_loaded():
    assert settings.app_name == "DraftForge"
    assert settings.app_version == "0.1.0"
    assert settings.debug == True