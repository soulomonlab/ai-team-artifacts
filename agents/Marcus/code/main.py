from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/items", response_model=schemas.ItemOut, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(db, item_in)
    return item


@app.get("/api/v1/items", response_model=List[schemas.ItemOut])
def list_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_items(db, skip=skip, limit=limit)


@app.get("/api/v1/items/{item_id}", response_model=schemas.ItemOut)
def get_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/api/v1/items/{item_id}", response_model=schemas.ItemOut)
def update_item_endpoint(item_id: int, item_upd: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = crud.update_item(db, item, item_upd)
    return updated


@app.delete("/api/v1/items/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return {"ok": True}
