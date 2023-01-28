from typing import Any
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx

from app.core.deps import get_db 
from app.currency.deps import get_from_currency_code, get_to_currency_code
from app.currency.scrapper import convert_currency, fetch_currencies
from app.currency.models import ConversionHistory
from app.currency.schemas import ConversionHistoryOut, ConversionHistoryMetadata, CurrenciesOut
from app.currency.exceptions import ParseException
from app.currency.types import CurrencyCodeT, CurrencyNameT


router = APIRouter()

@router.get("/convert", response_model=ConversionHistoryOut, responses={400: {'description': 'Wrong currenices'}})
async def convert(
    *,
    db: Session = Depends(get_db),
    amount: float,
    from_currency: CurrencyCodeT = Depends(get_from_currency_code),
    to_currency: CurrencyCodeT = Depends(get_to_currency_code)
) -> ConversionHistoryOut:
    convert_data = await convert_currency(amount, from_currency, to_currency)

    db_obj = ConversionHistory(
        amount=convert_data.amount,
        rate=convert_data.rate,
        time_of_conversion=convert_data.created_at,
        from_currency=from_currency,
        to_currency=to_currency,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return ConversionHistoryOut(
        converted_amount=db_obj.amount,
        rate=db_obj.rate,
        metadata=ConversionHistoryMetadata(
            time_of_conversion=db_obj.time_of_conversion,
            from_currency=db_obj.from_currency,
            to_currency=db_obj.to_currency,
        )
    )


@router.get("/currencies", response_model=CurrenciesOut, responses={424: {'description': 'Internal api request failure'}})
async def currencies() -> CurrenciesOut:
    return await fetch_currencies()


@router.get("/history", response_model=list[ConversionHistoryOut])
async def history(db: Session = Depends(get_db)) -> list[ConversionHistoryOut]:
    history = await db.execute(select(ConversionHistory))
    return [
        ConversionHistoryOut(
            converted_amount=db_obj.amount,
            rate=db_obj.rate,
            metadata=ConversionHistoryMetadata(
                time_of_conversion=db_obj.time_of_conversion,
                from_currency=db_obj.from_currency,
                to_currency=db_obj.to_currency,
            )
        ) for db_obj in history.scalars().all()
    ]
