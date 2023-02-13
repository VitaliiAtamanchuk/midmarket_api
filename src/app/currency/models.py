from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from app.core.db import Base
from app.currency.schemas import ConversionHistoryMetadata
from app.currency.schemas import ConversionHistoryOut


class ConversionHistory(Base):
    __tablename__ = 'conversion_histories'

    id = Column(Integer, primary_key=True)
    amount = Column('amount', Float(asdecimal=True), nullable=False)
    rate = Column(Float, nullable=False)
    time_of_conversion = Column(DateTime(timezone=True), nullable=False)
    from_currency = Column(String(3), nullable=False)
    to_currency = Column(String(3), nullable=False)

    def to_out(self) -> ConversionHistoryOut:
        return ConversionHistoryOut(
            converted_amount=self.amount,
            rate=self.rate,
            metadata=ConversionHistoryMetadata(
                time_of_conversion=self.time_of_conversion,
                from_currency=self.from_currency,
                to_currency=self.to_currency,
            ),
        )


async def create_conversion_history(
    db: Session,
    *,
    amount: float,
    rate: float,
    time_of_conversion: datetime,
    from_currency: str,
    to_currency: str,
) -> ConversionHistory:

    db_obj = ConversionHistory(
        amount=amount,
        rate=rate,
        time_of_conversion=time_of_conversion,
        from_currency=from_currency,
        to_currency=to_currency,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
