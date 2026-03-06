from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional, Dict, Any

def create_item(db: Session, item_in: schemas.ItemCreate, owner_id: Optional[int]=None) -> models.Item:
    db_item = models.Item(
        title=item_in.title,
        description=item_in.description,
        is_private=item_in.is_private,
        metadata=item_in.metadata or {},
        owner_id=owner_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # history
    create_history(db, db_item.id, changed_by=owner_id, change_type="create", payload={"item": db_item.title})
    return db_item

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def list_items(db: Session, skip: int=0, limit: int=50, q: Optional[str]=None) -> List[models.Item]:
    query = db.query(models.Item).order_by(models.Item.created_at.desc())
    if q:
        qlike = f"%{q}%"
        query = query.filter(models.Item.title.ilike(qlike) | models.Item.description.ilike(qlike))
    return query.offset(skip).limit(limit).all()

def update_item(db: Session, item: models.Item, changes: Dict[str, Any], changed_by: Optional[int]=None) -> models.Item:
    for k, v in changes.items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    create_history(db, item.id, changed_by=changed_by, change_type="update", payload=changes)
    return item

def delete_item(db: Session, item: models.Item, deleted_by: Optional[int]=None):
    create_history(db, item.id, changed_by=deleted_by, change_type="delete", payload={"id": item.id})
    db.delete(item)
    db.commit()

# History helpers

def create_history(db: Session, item_id: int, changed_by: Optional[int], change_type: str, payload: Dict[str, Any]):
    hist = models.ItemHistory(item_id=item_id, changed_by=changed_by, change_type=change_type, payload=payload)
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist

def list_history(db: Session, item_id: int):
    return db.query(models.ItemHistory).filter(models.ItemHistory.item_id == item_id).order_by(models.ItemHistory.created_at.desc()).all()
