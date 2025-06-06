from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest
from app import models
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
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
    user_date = {"email": "cc@gamil.com", "password": "123456"}
    res = client.post(
        "/users/", json=user_date)

    assert res.status_code == 201
    new_user = res.json()
    new_user['username'] = user_date['email']
    new_user['password'] = user_date['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_date = {"email": "ccc@gamil.com", "password": "123456"}
    res = client.post(
        "/users/", json=user_date)

    assert res.status_code == 201
    new_user = res.json()
    new_user['username'] = user_date['email']
    new_user['password'] = user_date['password']
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
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "1 title",
        "content": "1 content",
        "owner_id": test_user2['id']
    },
        {
        "title": "2 title",
        "content": "2 content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
