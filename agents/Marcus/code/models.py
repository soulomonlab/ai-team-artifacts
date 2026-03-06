"""
SQLAlchemy models for users, resources, and shares (permissions).
This is intentionally minimal and focused on the sharing/permissions domain.
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RoleEnum(str, Enum):
    OWNER = "owner"
    WRITE = "write"
    READ = "read"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")


class Share(Base):
    __tablename__ = "shares"
    __table_args__ = (
        UniqueConstraint("resource_id", "user_id", name="uq_resource_user"),
    )

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    invited_email = Column(String, nullable=True)
    role = Column(SAEnum(RoleEnum), nullable=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=True, unique=True)
    accepted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    resource = relationship("Resource")
    user = relationship("User", foreign_keys=[user_id])

