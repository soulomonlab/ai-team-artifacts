from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def create_item(db: Session, item_in: schemas.ItemCreate):
    item = models.Item(title=item_in.title, description=item_in.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    # create history entry
    hist = models.ItemHistory(item_id=item.id, title=item.title, description=item.description, version=item.version)
    db.add(hist)
    db.commit()
    return item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def list_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def update_item(db: Session, item: models.Item, updates: schemas.ItemUpdate):
    changed = False
    if updates.title is not None and updates.title != item.title:
        item.title = updates.title
        changed = True
    if updates.description is not None and updates.description != item.description:
        item.description = updates.description
        changed = True
    if updates.is_archived is not None and updates.is_archived != item.is_archived:
        item.is_archived = updates.is_archived
        changed = True
    if changed:
        item.version = item.version + 1 if item.version else 1
        item.updated_at = datetime.utcnow()
        db.add(item)
        db.commit()
        db.refresh(item)
        hist = models.ItemHistory(item_id=item.id, title=item.title, description=item.description, version=item.version)
        db.add(hist)
        db.commit()
    return item


def delete_item(db: Session, item: models.Item):
    db.delete(item)
    db.commit()
    return True
