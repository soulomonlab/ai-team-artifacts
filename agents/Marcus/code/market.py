from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from . import Base

class TopTicker(Base):
    __tablename__ = "top_tickers"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(255))
    exchange = Column(String(100))
    market_cap = Column(Numeric(30, 2))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
