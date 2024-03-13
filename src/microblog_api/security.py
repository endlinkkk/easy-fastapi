from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name="Api-Key", auto_error=False)


def check_access_token(api_key_header: str = Security(api_key_header)) -> str:
    return api_key_header
