import pytest
from app import models


@pytest.fixture()
def test_vote(session, test_posts, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_one_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    # post_id = test_posts[0].id
    # authorized_client.post(
    #     "/vote/", json={"post_id": post_id, "dir": 1})
    # res = authorized_client.post(
    #     "/vote/", json={"post_id": post_id, "dir": 1})
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 99999, "dir": 1})
    assert res.status_code == 404


def test_vot_on_unauthorized_user(client, test_posts):
    res = client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
