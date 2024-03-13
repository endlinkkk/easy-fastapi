from fastapi import APIRouter, status, Depends, UploadFile, File
from fastapi.security.api_key import APIKey
from typing import List
from src.microblog_api.schemas import (
    TweetCreateResponse,
    TweetCreateRequest,
    MediaCreateResponse,
    TweetsGetResponse,
    ProfileGetResponse,
    User,
    Tweet,
    Tags,
)
from src.microblog_api.security import check_access_token
from src.microblog_api import service
from src.database import get_session
from sqlalchemy.orm import Session
from loguru import logger

router = APIRouter()


@router.post(
    "/tweets",
    status_code=status.HTTP_201_CREATED,
    response_model=TweetCreateResponse,
    tags=[Tags.tweets],
)
def create_tweet(
    tweet: TweetCreateRequest,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> TweetCreateResponse:
    logger.info("Start create_tweet api")
    tweet_id = service.create_tweet(api=api_key, tweet=tweet, session=session)
    logger.info(f"tweet successfully added: ID = {tweet_id}")
    return {"result": True, "tweet_id": tweet_id}


@router.post(
    "/medias",
    status_code=status.HTTP_201_CREATED,
    response_model=MediaCreateResponse,
    tags=[Tags.medias],
)
def create_media(
    file: UploadFile = File(...),
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> MediaCreateResponse:
    logger.info(f"Media start work")
    media_id = service.create_media(api=api_key, file=file, session=session)
    return {"result": True, "media_id": media_id}


@router.delete("/tweets/{id}", status_code=status.HTTP_200_OK, tags=[Tags.tweets])
def delete_tweet(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    service.delete_tweet(tweet_id=id, api=api_key, session=session)
    return {"result": True}


@router.post(
    "/tweets/{id}/likes", status_code=status.HTTP_201_CREATED, tags=[Tags.tweets]
)
def add_like(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    service.create_like(tweet_id=id, api=api_key, session=session)
    return {"result": True}


@router.delete("/tweets/{id}/likes", status_code=status.HTTP_200_OK, tags=[Tags.tweets])
def delete_like(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    service.delete_like(tweet_id=id, api=api_key, session=session)
    return {"result": True}


@router.get(
    "/tweets",
    status_code=status.HTTP_200_OK,
    response_model=TweetsGetResponse,
    tags=[Tags.tweets],
)
def get_tweets(
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> TweetsGetResponse:
    tweets: List[Tweet] = service.get_all_tweets(session=session)
    logger.debug(f"get_all_tweets returned {tweets}")
    return TweetsGetResponse(result=True, tweets=tweets)


@router.post(
    "/users/{id}/follow", status_code=status.HTTP_201_CREATED, tags=[Tags.users]
)
def subscribe_to_user(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    service.create_follow(user_id=id, api=api_key, session=session)
    return {"result": True}


@router.delete("/users/{id}/follow", status_code=status.HTTP_200_OK, tags=[Tags.users])
def unsubscribe_from_user(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    service.delete_follow(user_id=id, api=api_key, session=session)
    return {"result": True}


@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=ProfileGetResponse,
    tags=[Tags.users],
)
def get_my_profile(
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> ProfileGetResponse:
    logger.info("Start get_my_profile")
    user = service.get_user_by_api(api="smile", session=session)
    logger.debug(f"get_user_by_api returned {user.name}")
    user_data = User(
        id=user.id, name=user.name, followers=user.followers, following=user.following
    )
    return ProfileGetResponse(result=True, user=user_data)


@router.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileGetResponse,
    tags=[Tags.users],
)
def get_user_profile(
    id: int,
    api_key: APIKey = Depends(check_access_token),
    session: Session = Depends(get_session),
) -> ProfileGetResponse:
    logger.info("Start get_user_profile")
    user = service.get_user_by_id(user_id=id, session=session)
    logger.debug(f"get_user_by_id returned {user.name}")
    user_data = User(
        id=user.id, name=user.name, followers=user.followers, following=user.following
    )
    return ProfileGetResponse(result=True, user=user_data)
