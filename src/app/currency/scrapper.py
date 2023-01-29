from datetime import datetime
import logging
import json
import contextvars
from collections import namedtuple

import bs4 
import httpx
from fastapi import HTTPException, status

from app.currency.contants import HEADERS, COOKIES
from app.core.scrapper import ScrapperClient, parse_handler
from app.currency.types import CurrencyCodeT
from app.currency.schemas import CurrenciesOut
from app.core.redis import make_keys, get_cache, set_cache


ConvertCurrencyResponse = namedtuple('ConvertCurrencyResponse', 'rate amount created_at')

async def fetch_currencies() -> CurrenciesOut:
    keys = make_keys()
    cached_currencies = await get_cache(keys)
    if cached_currencies: return cached_currencies

    async with ScrapperClient() as client:
        _, soup = await client.request_and_soup(
            'GET',
            'https://www.xe.com/currencyconverter/',
            headers=HEADERS,
            cookies=COOKIES
        )

    with parse_handler():
        currencies = json.loads(soup.select_one('#__NEXT_DATA__').text) \
            ['props']['pageProps']['commonI18nResources']['currencies']['en']
        
        currencies = dict((v['name'], k) for k,v in currencies.items())
        await set_cache(currencies, keys)
        return currencies


async def convert_currency(
    amount: float,
    from_currency_code: CurrencyCodeT,
    to_currency_code: CurrencyCodeT
) -> ConvertCurrencyResponse:
    async with ScrapperClient() as client:
        created_at = datetime.utcnow()
        response, soup = await client.request_and_soup(
            'GET',
            f'https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency_code}&To={to_currency_code}',
            headers=HEADERS,
            cookies=COOKIES
        )
        created_at += response.elapsed

    with parse_handler():
        amount = float(soup.select_one('.result__BigRate-sc-1bsijpp-1').get_text().split(" ")[0].replace(',', ''))

        paragraphs = soup.select('.unit-rates___StyledDiv-sc-1dk593y-0 p')
        rate = amount \
            if len(paragraphs) == 1 \
            else float(soup.select_one('.unit-rates___StyledDiv-sc-1dk593y-0 p').get_text().split(" ")[3].replace(',', ''))
        return ConvertCurrencyResponse(created_at=created_at, amount=amount, rate=rate)
