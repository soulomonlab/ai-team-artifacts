from datetime import datetime
from . import models, crud
from sqlalchemy.orm import Session
from celery import Celery

celery_app = Celery("worker", broker="redis://localhost:6379/0")


@celery_app.task
def publish_post_task(post_id: int):
    # Importing db session here would be application-specific; placeholder
    from .deps import get_db_session
    db: Session = get_db_session()
    post = crud.get_post(db, post_id)
    if not post:
        return
    post.status = models.PostStatus.published
    post.published_at = datetime.utcnow()
    db.add(post)
    db.commit()


def enqueue_publish(db: Session, post_id: int, scheduled_at: datetime):
    # Calculate ETA for celery
    eta = scheduled_at
    publish_post_task.apply_async(args=[post_id], eta=eta)
