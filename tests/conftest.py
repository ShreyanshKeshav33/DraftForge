import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.user import User
from app.core.config import settings
from app.database import Base

TEST_DATABASE_URL = "postgresql://draftforge:draftforge123@127.0.0.1:5433/draftforge_test"

engine= create_engine(TEST_DATABASE_URL)
TestingSessionLocal= sessionmaker(bind=engine)

def override_get_db():
    db= TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()        

