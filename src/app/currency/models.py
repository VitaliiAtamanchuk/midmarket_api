from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Float, DateTime
from sqlalchemy.orm import Session

from app.core.db import Base
from app.currency.schemas import ConversionHistoryOut, ConversionHistoryMetadata


class ConversionHistory(Base):
    __tablename__ = "conversion_histories"
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
        )
    )


async def create_conversion_history(db: Session, **kwargs):
    db_obj = ConversionHistory(
        amount=kwargs['amount'],
        rate=kwargs['rate'],
        time_of_conversion=kwargs['time_of_conversion'],
        from_currency=kwargs['from_currency'],
        to_currency=kwargs['to_currency'],
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
