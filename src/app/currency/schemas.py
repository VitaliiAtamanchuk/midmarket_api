from datetime import datetime

from pydantic import BaseModel


class ConversionHistoryMetadata(BaseModel):
    time_of_conversion: datetime 
    from_currency: str
    to_currency: str


class ConversionHistoryOut(BaseModel):
    converted_amount: float
    rate: float
    metadata: ConversionHistoryMetadata

