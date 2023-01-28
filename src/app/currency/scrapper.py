from datetime import datetime
import logging
import json
import contextvars
from collections import namedtuple

import bs4 
import httpx
from fastapi import HTTPException, status

from app.currency.contants import HEADERS, COOKIES
from app.currency.exceptions import ParseException
from app.core.scrapper import ScrapperClient
from app.currency.types import CurrencyCodeT
from app.currency.schemas import CurrenciesOut


ConvertCurrencyResponse = namedtuple('ConvertCurrencyResponse', 'rate amount created_at')

CURRENCIES = None
async def fetch_currencies() -> CurrenciesOut:
    # TODO:
    global CURRENCIES
    if CURRENCIES: return CURRENCIES

    async with ScrapperClient() as client:
        _, soup = await client.request_and_soup(
            'GET',
            'https://www.xe.com/currencyconverter/',
            headers=HEADERS,
            cookies=COOKIES
        )

    try:
        data = json.loads(soup.select_one('#__NEXT_DATA__').text)
        currencies = data['props']['pageProps']['commonI18nResources']['currencies']['en']
        CURRENCIES = dict((v['name'], k) for k,v in currencies.items())
    except Exception as exc:
        logging.critical("An exception happened", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail='Internal api request failure'
        )
    else:
        return CURRENCIES


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

    try:
        amount = float(soup.select_one('.result__BigRate-sc-1bsijpp-1').get_text().split(" ")[0].replace(',', ''))

        paragraphs = soup.select('.unit-rates___StyledDiv-sc-1dk593y-0 p')
        rate = amount \
            if len(paragraphs) == 1 \
            else float(soup.select_one('.unit-rates___StyledDiv-sc-1dk593y-0 p').get_text().split(" ")[3].replace(',', ''))
    except Exception as exc:
        logging.critical("An exception happened", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail='Internal api request failure'
        )
    else:
        return ConvertCurrencyResponse(created_at=created_at, amount=amount, rate=rate)
