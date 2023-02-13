import logging
from contextlib import contextmanager

import bs4
import httpx
from fastapi import HTTPException
from fastapi import status

from app.core import errors


class ScrapperClient(httpx.AsyncClient):
    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        try:
            return await super().request(method, url, **kwargs)
        except httpx.RequestError as exc:
            logging.critical('An exception happened', exc_info=exc)
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=errors.MSG_HTTP_424_FAILED_DEPENDENCY,
            )

    async def request_and_soup(self, method: str, url: str, **kwargs) -> tuple:
        response = await self.request(method, url, **kwargs)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return response, soup


@contextmanager
def parse_handler():
    try:
        yield
    except Exception as exc:
        logging.critical('An exception happened', exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=errors.MSG_HTTP_424_FAILED_DEPENDENCY,
        )
