from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FeedItemOut(BaseModel):
    id: int
    created_at: datetime
    content: str

    class Config:
        orm_mode = True

class FeedPage(BaseModel):
    items: List[FeedItemOut]
    next_cursor: Optional[str]

