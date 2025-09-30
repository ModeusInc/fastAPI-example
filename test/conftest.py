import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import models
from app.database import get_db, Base
from app.oauth2 import create_access_token

POSTGRESQL_DB_URL = "postgresql://postgres:Sanchez7@localhost:5432/fastapi_test"

engine = create_engine(POSTGRESQL_DB_URL)

TestingLocalSession = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingLocalSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "grishayaeger@gmail.com", "password": "13"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "grishayaege2@gmail.com", "password": "13"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "first title", 'content': 'bla bla',
            "owner_id": test_user['id']},
        {"title": "2nd title", 'content': 'spazzz',
            "owner_id": test_user['id']},
        {"title": "3rd title", 'content': 'weggo',
            "owner_id": test_user['id']},
        {"title": "3rd title", 'content': 'weggo', "owner_id": test_user2['id']}]

    def create_posts_model(post):
        return models.Post(**post)

    post_map = map(create_posts_model, posts_data)
    posts = list(post_map)  # Converts map to list

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

#    session.add_all([models.Post(title="first title", content='bla bla', owner_id=test_user['id']),
#                    models.Post(title="2nd title", content='spazzz',
#                                owner_id=test_user['id']),
#                    models.Post(title="3rd title", content='weggo', owner_id=test_user['id'])])
