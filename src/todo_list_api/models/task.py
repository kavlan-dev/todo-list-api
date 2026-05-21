from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from todo_list_api.models.user import Base


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    completed: Optional[bool] = Field(False, description="Статус выполнения задачи")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Название задачи"
    )
    description: Optional[str] = Field(None, description="Описание задачи")
    completed: Optional[bool] = Field(None, description="Статус выполнения задачи")


class TaskResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор задачи")
    title: str = Field(min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    completed: bool = Field(description="Статус выполнения задачи")
    user_id: int = Field(description="Идентификатор пользователя-владельца")
    created_at: datetime = Field(description="Дата и время создания задачи")
    updated_at: datetime = Field(
        description="Дата и время последнего обновления задачи"
    )

    class Config:
        from_attributes = True


class Task(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    owner = relationship("UserModel", back_populates="tasks")
