from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.currency.contants import CURRENCIES
from app.currency.deps import get_from_currency_code, get_to_currency_code
from app.currency.scrapper import fetch_currency
from app.currency.models import ConversionHistory
from app.core.deps import get_db 
from app.currency.schemas import ConversionHistoryOut, ConversionHistoryMetadata


router = APIRouter()


@router.get("/convert", response_model=ConversionHistoryOut)
async def convert(
    *,
    db: Session = Depends(get_db),
    amount: float,
    from_currency: str = Depends(get_from_currency_code),
    to_currency: str = Depends(get_to_currency_code)
) -> ConversionHistoryOut:
    data = await fetch_currency(amount, from_currency, to_currency)

    db_obj = ConversionHistory(
        amount=data['amount'],
        rate=data['rate'],
        time_of_conversion=data['created_at'],
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


@router.get("/currencies")
async def currencies():
    return CURRENCIES


@router.get("/history", response_model=list[ConversionHistoryOut])
async def history(db: Session = Depends(get_db)):
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
