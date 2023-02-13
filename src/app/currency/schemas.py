from datetime import datetime

from pydantic import BaseModel

from app.currency.types import CurrencyCodeT
from app.currency.types import CurrencyNameT


class CurrenciesOut(BaseModel):
    __root__: dict[CurrencyCodeT, CurrencyNameT]

    class Config:
        schema_extra = {
            'currency': 'currency name',
        }


class ConversionHistoryMetadata(BaseModel):
    time_of_conversion: datetime
    from_currency: str
    to_currency: str


class ConversionHistoryOut(BaseModel):
    converted_amount: float
    rate: float
    metadata: ConversionHistoryMetadata
