import os
from typing import Generator
import secrets

from fastapi import Security
from fastapi.security import APIKeyHeader

from app.core.db import SessionLocal


API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-KEY")


def get_api_key(api_key_header: str = Security(api_key_header)):
    if secrets.compare_digest(api_key_header, API_KEY):
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


async def get_db() -> Generator:
    async with SessionLocal() as db:
        yield db
