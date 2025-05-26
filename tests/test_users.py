from app import schemas
from jose import jwt
import pytest
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "cc@gamil.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "cc@gamil.com"


def test_login_user(client, test_user):

    res = client.post(
        "/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("username,password,status_code", [
    ('ccc@gamil.com', '123456', 403),
    ('cc@gamil.com', '0123456', 403),
    ('cc@gamil.com', None, 403)
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post(
        "/login", data={"username": username, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
