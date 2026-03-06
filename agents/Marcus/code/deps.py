from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from fastapi import Depends, HTTPException, status
from .models import Base, Post
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI dependency

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Placeholder auth

def get_current_user():
    class User:
        id = 1
    return User()
