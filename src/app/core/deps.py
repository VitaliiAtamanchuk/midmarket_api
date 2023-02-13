import os
import secrets
from typing import AsyncGenerator
from typing import Final

from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import APIKeyHeader

from app.core.db import SessionLocal


API_KEY: Final = os.getenv('API_KEY', '')
api_key_header_dep = APIKeyHeader(name='X-API-KEY')


def get_api_key(api_key_header: str = Security(api_key_header_dep)) -> str:
    if api_key_header and secrets.compare_digest(api_key_header, API_KEY):
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate API KEY',
        )


async def get_db() -> AsyncGenerator:
    async with SessionLocal() as db:
        yield db
