from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ItemBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_archived: Optional[bool] = None


class ItemVersionSchema(BaseModel):
    id: int
    item_id: int
    title: str
    description: Optional[str]
    version_number: int
    created_at: datetime

    class Config:
        orm_mode = True


class ItemSchema(ItemBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    versions: List[ItemVersionSchema] = []

    class Config:
        orm_mode = True
