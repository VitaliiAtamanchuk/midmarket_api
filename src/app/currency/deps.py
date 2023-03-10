from fastapi import HTTPException
from fastapi import Query

from app.currency.scrapper import fetch_currencies
from app.currency.types import CurrencyCodeT


class DepsFactory:
    @classmethod
    def create_get_currency_code(cls, alias: str):
        async def func(code: CurrencyCodeT = Query(..., alias=alias)):
            currencies = await fetch_currencies()
            currencies_code = list(currencies.values())
            if code not in currencies_code:
                raise HTTPException(status_code=400, detail='Invalid currency code')
            return code
        return func

get_from_currency_code = DepsFactory.create_get_currency_code('from_currency')
get_to_currency_code = DepsFactory.create_get_currency_code('to_currency')
