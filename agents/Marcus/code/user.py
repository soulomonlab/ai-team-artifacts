from sqlalchemy import Column, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column("email", nullable=False, unique=True, index=True)
    full_name = Column("full_name", nullable=True)
    metadata = Column(JSONB, nullable=False, server_default='{}')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_users_metadata", "metadata", postgresql_using="gin"),
    )
