from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(
        min_length=8, max_length=100, description="Пароль пользователя"
    )


class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    password: str = Field(
        min_length=8, max_length=100, description="Пароль пользователя"
    )


class UserResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор пользователя")
    username: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    created_at: datetime = Field(description="Дата и время создания пользователя")
    updated_at: datetime = Field(
        description="Дата и время последнего обновления пользователя"
    )

    class Config:
        from_attributes = True


class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    tasks = relationship(
        "TaskModel", back_populates="owner", cascade="all, delete-orphan"
    )
