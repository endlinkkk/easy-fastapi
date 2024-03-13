from typing import Any, List
import uuid
from src.microblog_api.schemas import TweetCreateRequest
from src.database import User, Tweet, Like, Image
from src.microblog_api.serializers import tweets_serializers
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from loguru import logger

import os


IMAGEDIR = "/usr/share/nginx/html/static/images/"


def get_user_by_id(user_id: int, session: Session) -> User | None:
    logger.info("Start get_user_by_id")
    select_query = select(User).where(User.id == user_id)
    return session.scalars(select_query).one()


def get_user_by_api(api: str, session: Session) -> User | None:
    logger.info("Start get_user_by_api")
    select_query = select(User).where(User.api == api)
    return session.scalars(select_query).one()


def get_image_by_id(id: int, session: Session) -> Image:
    select_query = select(Image).where(Image.id == id)
    return session.scalar(select_query)


def create_tweet(api: str, tweet: TweetCreateRequest, session: Session) -> int:
    logger.info("Start create_tweet")
    user = get_user_by_api(api=api, session=session)
    links = [get_image_by_id(image_id, session) for image_id in tweet.tweet_media_ids]
    if user:
        new_tweet = Tweet(
            content=tweet.tweet_data, attachment=links, author_id=user.id, like=[]
        )
        session.add(new_tweet)
        session.flush()
        new_id = new_tweet.id
        session.commit()
        return new_id
    else:
        raise


def get_all_tweets(session: Session) -> List[Tweet]:
    logger.info("Start get_all_tweets")
    select_query = select(Tweet)
    unserialized_tweets = session.scalars(select_query).all()
    serialized_tweets = tweets_serializers(unserialized_tweets)
    return serialized_tweets


def delete_tweet(tweet_id: int, api: str, session: Session) -> None:
    logger.info("Start delete_tweets")
    user = get_user_by_api(api=api, session=session)
    delete_query = delete(Tweet).where(Tweet.id == tweet_id, Tweet.author_id == user.id)
    session.execute(delete_query)
    session.commit()


def create_like(tweet_id: int, api: str, session: Session) -> None:
    logger.info("Start create_like")
    user = get_user_by_api(api=api, session=session)
    like = Like(tweet_id=tweet_id, author_id=user.id)
    session.add(like)
    session.commit()


def delete_like(tweet_id: int, api: str, session: Session) -> None:
    logger.info("Start delete_like")
    user = get_user_by_api(api=api, session=session)
    delete_query = delete(Like).where(
        Like.tweet_id == tweet_id, Like.author_id == user.id
    )
    session.execute(delete_query)
    session.commit()


def create_follow(user_id: int, api: str, session: Session) -> None:
    logger.info("Start create_follow")
    user = get_user_by_api(api=api, session=session)
    following_user = session.get(User, user_id)
    user.following.append(following_user)
    session.commit()


def delete_follow(user_id: int, api: str, session: Session) -> None:
    logger.info("Start delete_follow")
    user = get_user_by_api(api=api, session=session)
    unfollowing_user = session.get(User, user_id)
    user.following.remove(unfollowing_user)
    session.commit()


def create_media(api: str, file, session: Session) -> int:
    logger.info("Start create_media")
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = file.file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    new_image = Image(link=f"http://127.0.0.1:80/images/{file.filename}")
    session.add(new_image)
    session.commit()
    return new_image.id
