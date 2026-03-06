from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, deps, crud

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])


@router.post("/", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.PostCreate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    post = crud.create_post(db, author_id=current_user.id, payload=payload)
    return post


@router.get("/", response_model=List[schemas.PostOut])
def list_posts(status: str = None, skip: int = 0, limit: int = 20, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    posts = crud.list_posts(db, author_id=current_user.id, status=status, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    post = crud.get_post(db, post_id=post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, payload: schemas.PostUpdate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user), background_tasks: BackgroundTasks = Depends()):
    post = crud.get_post(db, post_id=post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    post = crud.update_post(db, post, payload)
    # if scheduled -> enqueue background job
    if post.status == models.PostStatus.scheduled and post.scheduled_at:
        from ..tasks import enqueue_publish
        enqueue_publish(db, post.id, post.scheduled_at)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    post = crud.get_post(db, post_id=post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.delete_post(db, post)
    return None
