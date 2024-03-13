from typing import List, Generator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from .config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}", echo=True
)
session_maker = sessionmaker(engine, class_=Session)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    api: Mapped[str] = mapped_column(String(40), nullable=False)
    following: Mapped[List["User"] | None] = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref="followers",
    )
    tweet: Mapped[List["Tweet"] | None] = relationship(back_populates="author")
    like: Mapped[List["Like"] | None] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User: {self.id}"


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("following_id", Integer, ForeignKey(User.id), primary_key=True),
)


class Like(Base):
    __tablename__ = "like_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tweet_table.id", ondelete="CASCADE")
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    author: Mapped["User"] = relationship(back_populates="like")

    @classmethod
    def get_by_ids(cls, tweet_id, user_id) -> "Like":
        return cls.query.get(tweet_id, user_id)

    def to_json(self) -> dict:
        return {
            "tweet_id": self.tweet_id,
            "user_id": self.author_id,
        }


class Tweet(Base):
    __tablename__ = "tweet_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(280), nullable=False)
    attachment: Mapped[List["Image"] | None] = relationship(
        "Image",
        back_populates="tweet",
        cascade="all, delete",
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    author: Mapped["User"] = relationship(back_populates="tweet")
    like: Mapped[List["Like"] | None] = relationship(
        "Like",
        backref="tweet",
        cascade="all, delete",
    )

    @classmethod
    def get_by_id(cls, tweet_id) -> "Tweet":
        return cls.query.get_or_404(tweet_id)


class Image(Base):
    __tablename__ = "image_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tweet_table.id", ondelete="CASCADE"), nullable=True
    )
    tweet: Mapped["Tweet"] = relationship(back_populates="attachment", post_update=True)
    link: Mapped[str] = mapped_column(String(255), nullable=True)

    def to_json(self, url_pattern) -> dict:
        return {
            "image_id": self.id,
            "tweet_id": self.tweet_id,
            "url": url_pattern.format(id=self.id),
        }


def get_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session


def add_fake_user() -> None:
    session = next(get_session())
    fake_user = User(name="Catalyst", api="smile")
    session.add(fake_user)
    session.commit()


def check_content() -> Boolean:
    session = next(get_session())
    return True if session.query(User).count() else False


def create_db() -> None:
    Base.metadata.create_all(engine)
