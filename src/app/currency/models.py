from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Float, DateTime

from app.core.db import Base


class ConversionHistory(Base):
    __tablename__ = "conversion_histories"
    id = Column(Integer, primary_key=True)

    amount = Column('amount', Float(asdecimal=True), nullable=False)
    rate = Column(Float, nullable=False)
    
    time_of_conversion = Column(DateTime(timezone=True), nullable=False)
    from_currency = Column(String(3), nullable=False)
    to_currency = Column(String(3), nullable=False)
