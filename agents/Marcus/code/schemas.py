from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"
    deleted = "deleted"

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class PostCreate(PostBase):
    status: Optional[PostStatus] = PostStatus.draft

class PostUpdate(PostBase):
    status: Optional[PostStatus]

class PostOut(PostBase):
    id: int
    author_id: int
    status: PostStatus
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class AnalyticsOut(BaseModel):
    post_id: int
    views: int
    likes: int
    shares: int
    comments: int

    class Config:
        orm_mode = True
