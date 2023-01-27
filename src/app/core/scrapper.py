import logging

import httpx
from fastapi import HTTPException, status


async def get_response(url: str, headers: dict, cookies: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, cookies=cookies)
            return response
    except httpx.RequestError as exc:
        logging.critical("An exception happened", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail='Internal api request failure'
        )
