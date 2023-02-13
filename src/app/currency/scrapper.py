import json
from datetime import datetime
from typing import NamedTuple

from app.core.redis import get_cache
from app.core.redis import make_keys
from app.core.redis import set_cache
from app.core.scrapper import parse_handler
from app.core.scrapper import ScrapperClient
from app.currency.contants import COOKIES
from app.currency.contants import HEADERS
from app.currency.schemas import CurrenciesOut
from app.currency.types import CurrencyCodeT


class ConvertCurrencyResponse(NamedTuple):
    rate: float
    amount: float
    created_at: datetime


async def fetch_currencies() -> CurrenciesOut:
    keys = make_keys()
    cached_currencies = await get_cache(keys)
    if cached_currencies: return cached_currencies

    async with ScrapperClient() as client:
        _, soup = await client.request_and_soup(
            'GET',
            'https://www.xe.com/currencyconverter/',
            headers=HEADERS,
            cookies=COOKIES,
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
    to_currency_code: CurrencyCodeT,
) -> ConvertCurrencyResponse:
    async with ScrapperClient() as client:
        created_at = datetime.utcnow()
        response, soup = await client.request_and_soup(
            'GET',
            'https://www.xe.com/currencyconverter/convert/'
            f'?Amount={amount}&From={from_currency_code}&To={to_currency_code}',
            headers=HEADERS,
            cookies=COOKIES,
        )
        created_at += response.elapsed

    with parse_handler():
        amount_str = (
            soup.select_one('.result__BigRate-sc-1bsijpp-1')
            .get_text()
            .split(' ')[0]
            .replace(',', '')
        )

        paragraphs = soup.select('.unit-rates___StyledDiv-sc-1dk593y-0 p')
        rate_str = amount_str \
            if len(paragraphs) == 1 \
            else (
                soup.select_one('.unit-rates___StyledDiv-sc-1dk593y-0 p')
                .get_text()
                .split(' ')[3]
                .replace(',', '')
            )
        return ConvertCurrencyResponse(
            created_at=created_at,
            amount=float(amount_str),
            rate=float(rate_str),
        )
