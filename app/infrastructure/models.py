from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

try:
    # For PostgreSQL
    from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
    UUID_TYPE = PostgresUUID(as_uuid=True)
except ImportError:
    # For SQLite
    from sqlalchemy import String as SQLiteString
    UUID_TYPE = SQLiteString(36)

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    todos = relationship("TodoModel", back_populates="user")


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(UUID_TYPE, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="todos")
