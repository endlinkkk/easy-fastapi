from enum import Enum
from typing import List
from pydantic import BaseModel, HttpUrl, FileUrl


class Tags(Enum):
    tweets = "tweets"
    users = "users"
    medias = "medias"


class Author(BaseModel):
    id: int
    name: str


class Like(BaseModel):
    user_id: int
    name: str


class Tweet(BaseModel):
    id: int
    content: str
    attachments: List[str] = None
    author: Author
    likes: List[Like] = None


class TweetCreateRequest(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] = None


class TweetCreateResponse(BaseModel):
    result: bool
    tweet_id: int


class MediaCreateResponse(BaseModel):
    result: bool
    media_id: int


class MediaCreateRequest(BaseModel):
    form: bytes


class TweetsGetResponse(BaseModel):
    result: bool
    tweets: List[Tweet]


class Follow(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    name: str
    followers: List[Follow]
    following: List[Follow]


class ProfileGetResponse(BaseModel):
    result: bool
    user: User
