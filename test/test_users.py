from jose import jwt
import pytest
from app import schemas
from app.config import settings

# Lets test the root path


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "grishayaeger@gmail.com", "password": "13"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "grishayaeger@gmail.com"
    assert res.status_code == 201


def test_user_login(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '13', 403),
    ('grishayaeger@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'worngpassword', 403),
    (None, '13', 422),
    ('grishayaeger@gmail.com', None, 422)])
def test_failed_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
