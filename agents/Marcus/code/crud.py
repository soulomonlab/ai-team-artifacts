from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from sqlalchemy import select

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()

def list_posts(db: Session, skip: int = 0, limit: int = 20, status: str = None):
    q = db.query(models.Post).filter(models.Post.is_deleted == False)
    if status:
        q = q.filter(models.Post.status == models.PostStatus(status))
    return q.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def create_post(db: Session, author_id: int, post_in: schemas.PostCreate):
    db_post = models.Post(
        author_id=author_id,
        title=post_in.title,
        content=post_in.content,
        status=models.PostStatus(post_in.status),
        scheduled_at=post_in.scheduled_at,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # create analytics row
    analytics = models.PostAnalytics(post_id=db_post.id)
    db.add(analytics)
    db.commit()
    return db_post

def update_post(db: Session, post_id: int, post_in: schemas.PostUpdate):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()
    if not post:
        return None
    if post_in.title is not None:
        post.title = post_in.title
    if post_in.content is not None:
        post.content = post_in.content
    if post_in.status is not None:
        post.status = models.PostStatus(post_in.status)
        if post.status == models.PostStatus.PUBLISHED:
            post.published_at = datetime.utcnow()
    if post_in.scheduled_at is not None:
        post.scheduled_at = post_in.scheduled_at
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def soft_delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()
    if not post:
        return None
    post.is_deleted = True
    post.status = models.PostStatus.DELETED
    db.add(post)
    db.commit()
    return post

def increment_analytics(db: Session, post_id: int, views: int = 0, likes: int = 0):
    analytics = db.query(models.PostAnalytics).filter(models.PostAnalytics.post_id == post_id).first()
    if not analytics:
        analytics = models.PostAnalytics(post_id=post_id, views=views, likes=likes)
        db.add(analytics)
    else:
        analytics.views += views
        analytics.likes += likes
    db.commit()
    return analytics
