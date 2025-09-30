from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/p/")
    print(res.json())

    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    post_list = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/p")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/p{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/p/888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome title", "awesome content", True),
    ("Faaaaaaa", "GRAAAAAAAA", True),
    ("tallest man alive", "yea i said it", False)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "why why why", "content": "gift"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "why why why"
    assert created_post.content == "gift"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "why why why", "content": "gift"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_nonexistent_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/888")
    assert res.status_code == 404


def test_delete_other_users_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated one",
        "content": "belated one",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_another_users_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated one",
        "content": "belated one",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_nonexistent_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated one",
        "content": "belated one",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/888", json=data)

    assert res.status_code == 404
