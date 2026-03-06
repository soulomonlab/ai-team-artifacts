from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models import Post, PostStatus
from ..schemas import PostCreate, PostUpdate, PostOut
from ..database import get_db
from ..tasks import enqueue_publish_job

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user=Depends(...)):
    post = Post(
        title=payload.title,
        body=payload.body,
        author_id=current_user.id,
        is_public=payload.is_public,
    )
    if payload.scheduled_at:
        post.status = PostStatus.SCHEDULED
        post.scheduled_at = payload.scheduled_at
    db.add(post)
    db.commit()
    db.refresh(post)

    if post.status == PostStatus.SCHEDULED:
        enqueue_publish_job(db, post.id, post.scheduled_at)

    return post

@router.get("/", response_model=List[PostOut])
def list_posts(status: PostStatus = None, limit: int = 20, offset: int = 0, db: Session = Depends(get_db), current_user=Depends(...)):
    q = db.query(Post).filter(Post.author_id == current_user.id)
    if status:
        q = q.filter(Post.status == status)
    posts = q.order_by(Post.created_at.desc()).limit(limit).offset(offset).all()
    return posts

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(...)):
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db), current_user=Depends(...)):
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(post, field, value)
    # handle scheduling
    if payload.scheduled_at:
        post.status = PostStatus.SCHEDULED
        enqueue_publish_job(db, post.id, post.scheduled_at)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(...)):
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.status = PostStatus.DELETED
    db.commit()
    return None
