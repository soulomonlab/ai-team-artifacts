from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, crud_items

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items Service", version="1.0.0")


@app.post("/api/v1/items", response_model=schemas.ItemSchema, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud_items.create_item(db, item)
    return db_item


@app.get("/api/v1/items", response_model=List[schemas.ItemSchema])
def list_items(page: int = 1, size: int = 20, search: Optional[str] = None, db: Session = Depends(get_db)):
    skip = (page - 1) * size
    items = crud_items.list_items(db, skip=skip, limit=size, search=search)
    return items


@app.get("/api/v1/items/{item_id}", response_model=schemas.ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud_items.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/api/v1/items/{item_id}", response_model=schemas.ItemSchema)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated = crud_items.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@app.delete("/api/v1/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    ok = crud_items.delete_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}
