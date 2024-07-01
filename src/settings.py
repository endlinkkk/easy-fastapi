from functools import lru_cache
import environ

from pydantic_settings import BaseSettings

env = environ.Env()
environ.Env.read_env('.env')

class ProjectSettings(BaseSettings):
    POSTGRES_USER: str = env('POSTGRES_USER')
    POSTGRES_PASSWORD: str = env('POSTGRES_PASSWORD')
    POSTGRES_DB: str = env('POSTGRES_DB')
    POSTGRES_PORT: int = env('POSTGRES_PORT')
    SECRET_API: str = env('SECRET_API')

@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()