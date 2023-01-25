from fastapi import HTTPException, Depends, Query

from app.currency.contants import CURRENCIES_CODE


class DepsFactory:

    @classmethod
    def create_get_currency_code(cls, alias: str):
        def func(code: str = Query(..., alias=alias)):
            if code not in CURRENCIES_CODE:
                raise HTTPException(status_code=400, detail='Invalid currency code')
            return code
        return func

get_from_currency_code = DepsFactory.create_get_currency_code('from_currency')
get_to_currency_code = DepsFactory.create_get_currency_code('to_currency')
