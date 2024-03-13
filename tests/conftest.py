import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.main import app
from sqlalchemy.orm import sessionmaker
from httpx import Client
from src.database import Base, get_session


DATABASE_URL_TEST = "sqlite:///testdb.db"


engine_test = create_engine(DATABASE_URL_TEST)
session_maker = sessionmaker(bind=engine_test, class_=Session, expire_on_commit=False)
Base.metadata.bind = engine_test


def override_get_session() -> Session:
    with session_maker() as session:
        return session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    with engine_test.begin() as conn:
        Base.metadata.create_all(conn)
    yield
    with engine_test.begin() as conn:
        Base.metadata.drop_all(conn)


client = TestClient(app)
