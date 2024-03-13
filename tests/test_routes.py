from fastapi.testclient import TestClient
from conftest import client, session_maker
from src.database import User
from src.microblog_api.schemas import ProfileGetResponse
from pydantic import model_serializer

import os


def test_read_main():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add_user1():
    with session_maker() as session:
        fake_user = User(name="Catalyst", api="smile")
        session.add(fake_user)
        session.commit()


def test_get_user_by_id():
    headers = {"Api-Key": "smile"}
    response = client.get("api/users/1", headers=headers)
    assert response.json() == {
        "result": True,
        "user": {"id": 1, "name": "Catalyst", "followers": [], "following": []},
    }


def test_get_user_by_api():
    headers = {"Api-Key": "smile"}
    response = client.get("api/users/me", headers=headers)
    assert response.json() == {
        "result": True,
        "user": {"id": 1, "name": "Catalyst", "followers": [], "following": []},
    }


def test_add_tweet_by_user1():
    data = {"tweet_data": "First tweet by Catalyst", "tweet_media_ids": []}
    headers = {"Api-Key": "smile"}
    response = client.post(f"api/tweets", headers=headers, json=data)
    assert response.json() == {"result": True, "tweet_id": 1}


def test_delete_tweet():
    headers = {"Api-Key": "smile"}
    response = client.delete("/api/tweets/1", headers=headers)
    assert response.json() == {"result": True}
    response = client.get("api/tweets", headers=headers)
    expected_response = {"result": True, "tweets": []}
    assert response.json() == expected_response


def test_add_like():
    test_add_tweet_by_user1()
    headers = {"Api-Key": "smile"}
    response = client.post("/api/tweets/1/likes", headers=headers)
    assert response.json() == {"result": True}


def test_delete_like():
    headers = {"Api-Key": "smile"}
    response = client.delete("/api/tweets/1/likes", headers=headers)
    assert response.json() == {"result": True}


def test_add_user2():
    with session_maker() as session:
        fake_user = User(name="Mika", api="go")
        session.add(fake_user)
        session.commit()


def test_add_follow():
    headers = {"Api-Key": "smile"}
    response = client.post("/api/users/2/follow", headers=headers)
    assert response.json() == {"result": True}


def test_delete_follow():
    headers = {"Api-Key": "smile"}
    response = client.delete("/api/users/2/follow", headers=headers)
    assert response.json() == {"result": True}
