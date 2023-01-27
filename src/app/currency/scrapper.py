from datetime import datetime
import logging
import json

import bs4 
import httpx
from fastapi import HTTPException, status

from app.currency.contants import HEADERS, COOKIES
from app.currency.exceptions import ParseException
from app.core.scrapper import get_response


CURRENCIES = None
async def fetch_currencies():
    # TODO: dist redis cache
    global CURRENCIES
    if CURRENCIES: return CURRENCIES

    url = f'https://www.xe.com/currencyconverter/'
    response = await get_response(url, headers=HEADERS, cookies=COOKIES)
    soup = bs4.BeautifulSoup(response.text, "lxml")

    try:
        data = json.loads(soup.select_one('#__NEXT_DATA__').text)
        currencies = data['props']['pageProps']['commonI18nResources']['currencies']['en']
        CURRENCIES = dict((v['name'], k) for k,v in currencies.items())
        return CURRENCIES

    except Exception as exc:
        logging.critical("An exception happened", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail='Internal api request failure'
        )


async def convert_currency(amount: float, from_currency_code: str, to_currency_code: str):
    url = f'https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency_code}&To={to_currency_code}'
    response = await get_response(url, headers=HEADERS, cookies=COOKIES)
    created_at = datetime.utcnow() - response.elapsed
    soup = bs4.BeautifulSoup(response.text, "lxml")

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
    
    return {
        "rate": rate,
        "amount": amount,
        "created_at": created_at
    }
