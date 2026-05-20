from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(
        min_length=8, max_length=100, description="Пароль пользователя"
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(
        min_length=8, max_length=100, description="Пароль пользователя"
    )


class UserResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор пользователя")
    name: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    created_at: datetime = Field(description="Дата и время создания пользователя")
    updated_at: datetime = Field(
        description="Дата и время последнего обновления пользователя"
    )

    class Config:
        from_attributes = True
