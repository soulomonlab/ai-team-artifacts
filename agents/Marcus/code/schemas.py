from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_archived: Optional[bool]

class ItemHistoryOut(BaseModel):
    id: int
    item_id: int
    title: str
    description: Optional[str]
    changed_at: datetime
    version: int

    class Config:
        orm_mode = True

class ItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    version: int
    history: List[ItemHistoryOut] = []

    class Config:
        orm_mode = True
