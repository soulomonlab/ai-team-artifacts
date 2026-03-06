from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import SessionLocal, engine
from .. import models, schemas, crud
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple auth stub: in real system replace with JWT dependency

def get_current_user_id():
    # For now return fixed user id
    return 1

@router.post("/", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post_in: schemas.PostCreate, db: Session = Depends(get_db)):
    author_id = get_current_user_id()
    post = crud.create_post(db, author_id, post_in)
    # If scheduled, enqueue job (stub: return job id)
    if post.status == models.PostStatus.SCHEDULED and post.scheduled_at:
        # In real implementation, enqueue via Celery/RQ. Return scheduling id.
        job_id = str(uuid.uuid4())
        # Save job_id somewhere or create schedule record (omitted)
        return post
    return post

@router.get("/", response_model=List[schemas.PostOut])
def list_posts(page: int = 1, size: int = 20, status: Optional[schemas.PostStatus] = None, db: Session = Depends(get_db)):
    skip = (page - 1) * size
    status_filter = status.value if status else None
    posts = crud.list_posts(db, skip=skip, limit=size, status=status_filter)
    return posts

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post_in: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, post_in)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # If changed to scheduled, return job id stub
    if post.status == models.PostStatus.SCHEDULED and post.scheduled_at:
        job_id = str(uuid.uuid4())
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.soft_delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "deleted"}

@router.get("/{post_id}/analytics", response_model=schemas.AnalyticsOut)
def get_analytics(post_id: int, db: Session = Depends(get_db)):
    analytics = db.query(models.PostAnalytics).filter(models.PostAnalytics.post_id == post_id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics

# Scheduling endpoint: enqueue a publish job
@router.post("/{post_id}/schedule")
def schedule_post(post_id: int, when: datetime, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.scheduled_at = when
    post.status = models.PostStatus.SCHEDULED
    db.add(post)
    db.commit()
    # In production, enqueue Celery job to publish at `when`.
    job_id = str(uuid.uuid4())
    return {"job_id": job_id, "scheduled_at": when}
