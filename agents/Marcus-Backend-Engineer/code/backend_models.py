from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, create_engine, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class RoleEnum(str, Enum):
    OWNER = "owner"
    WRITE = "write"
    READ = "read"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    role = Column(SAEnum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    resource = relationship("Resource")

class InviteToken(Base):
    __tablename__ = "invite_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    role = Column(SAEnum(RoleEnum), nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resource = relationship("Resource")

# Simple DB setup for local tests/dev
engine = create_engine("sqlite:///./test_db.sqlite", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
