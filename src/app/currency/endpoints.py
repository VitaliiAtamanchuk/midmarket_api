from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.currency.deps import get_from_currency_code
from app.currency.deps import get_to_currency_code
from app.currency.models import ConversionHistory
from app.currency.models import create_conversion_history
from app.currency.schemas import ConversionHistoryOut
from app.currency.schemas import CurrenciesOut
from app.currency.scrapper import convert_currency
from app.currency.scrapper import fetch_currencies
from app.currency.types import CurrencyCodeT


router = APIRouter()


@router.get(
    '/convert',
    response_model=ConversionHistoryOut,
    responses={400: {'description': 'Wrong currenices'}},
)
async def convert(
    *,
    db: Session = Depends(get_db),
    amount: float,
    from_currency: CurrencyCodeT = Depends(get_from_currency_code),
    to_currency: CurrencyCodeT = Depends(get_to_currency_code),
) -> ConversionHistoryOut:
    convert_data = await convert_currency(amount, from_currency, to_currency)
    db_obj = await create_conversion_history(
        db,
        amount=convert_data.amount,
        rate=convert_data.rate,
        time_of_conversion=convert_data.created_at,
        from_currency=from_currency,
        to_currency=to_currency,
    )
    return db_obj.to_out()


@router.get(
    '/currencies',
    response_model=CurrenciesOut,
    responses={424: {'description': 'Internal api request failure'}},
)
async def currencies() -> CurrenciesOut:
    return await fetch_currencies()


@router.get('/history', response_model=list[ConversionHistoryOut])
async def history(db: Session = Depends(get_db)) -> list[ConversionHistoryOut]:
    history = await db.execute(select(ConversionHistory))
    return [
        db_obj.to_out() for db_obj in history.scalars().all()
    ]
