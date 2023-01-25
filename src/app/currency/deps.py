from fastapi import HTTPException, Depends, Query

from app.currency.contants import CURRENCIES


class DepsFactory:

    @classmethod
    def create_get_currency_code(cls, alias: str):
        def func(currency_name: str = Query(..., alias=alias)):
            code = CURRENCIES.get(currency_name, None)
            if not code:
                raise HTTPException(status_code=400, detail='Invalid currency name')
            return code
        return func

get_from_currency_code = DepsFactory.create_get_currency_code('from_currency')
get_to_currency_code = DepsFactory.create_get_currency_code('to_currency')
