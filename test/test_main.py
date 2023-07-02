import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from db.database import Base
from .test_utils import register_testing_user


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


user1_email = "test1@gmail.com"
user1_password = "test1_password"


def test_register(client):
    response = register_testing_user(client, user1_email)
    assert response.status_code == 200
    assert response.json() == {"email": user1_email, "id": 1}


def test_register_existing_email(client):
    register_testing_user(client, user1_email, "somepassword")
    response = register_testing_user(client, user1_email, "anotherpassword")
    assert response.status_code == 400


def test_register_then_login_with_correct_password(client):
    register_testing_user(client, user1_email, user1_password)
    response = client.post("/login", json={"email": user1_email, "password": user1_password})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "Bearer"


def test_register_then_login_with_incorrect_password(client):
    register_testing_user(client, user1_email, user1_password)
    response = client.post("/login", json={"email": user1_email, "password": user1_password + "wrong_suffix"})
    assert response.status_code == 400


def test_transactions(client):
    register_testing_user(client, user1_email, user1_password)
    login_response = client.post("/login", json={"email": user1_email, "password": user1_password})
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    response = client.get(
        "/transactions?address=0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    if len(response.json()) > 0:
        assert response.json()[0]["transactionHash"] is not None
        assert response.json()[0]["blockHash"] is not None


def test_transactions_with_no_authorization(client):
    response = client.get("/transactions?address=0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326")
    assert response.status_code == 403


def test_transactions_with_invalid_authorization(client):
    response = client.get(
        "/transactions?address=0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326",
        headers={"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  f".eyJ1c2VyX2lkIjo2LCJleHAiOjE2ODgzMTMwMTF9"
                                  f".wd_HXQJcTj460zfHNV0tVHLomdsKiRm8RrdeQCpJ-WU"}
    )
    assert response.status_code == 401
