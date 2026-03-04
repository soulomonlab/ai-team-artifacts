from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TopTickerOut(BaseModel):
    ticker: str
    name: Optional[str]
    exchange: Optional[str]
    market_cap: Optional[float]
    fetched_at: Optional[datetime]

    class Config:
        orm_mode = True
