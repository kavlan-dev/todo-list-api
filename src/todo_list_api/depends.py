import os
from typing import Any, Dict, Generator

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session

from todo_list_api.config import Config, CORSConfig, DBConfig
from todo_list_api.db import Database
from todo_list_api.models.task import Task
from todo_list_api.models.user import User
from todo_list_api.repositories.task import (
    ITaskRepository,
    InMemoryTaskRepository,
    PostgreSQLTaskRepository,
)
from todo_list_api.repositories.user import (
    InMemoryUserRepository,
    IUserRepository,
    PostgreSQLUserRepository,
)
from todo_list_api.services.task import TaskService
from todo_list_api.services.user import UserService
from todo_list_api.utils.security import JWTAuth


def get_config() -> Config:
    load_dotenv()
    allow_origins_str = os.getenv("ALLOW_ORIGINS", "*")
    allow_origins = (
        [origin.strip() for origin in allow_origins_str.split(",")]
        if allow_origins_str != "*"
        else ["*"]
    )

    cfg = Config(
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", ""),
        env=os.getenv("ENV", "local"),
        db_cfg=DBConfig(
            user=os.getenv("POSTGRES_USER", ""),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            name=os.getenv("POSTGRES_DB", ""),
        ),
        cors_cfg=CORSConfig(allow_origins=allow_origins),
    )
    return cfg


def get_jwt_auth(cfg: Config = Depends(get_config)) -> JWTAuth:
    return JWTAuth(cfg.jwt_secret_key)


def get_db(cfg: Config) -> Generator[Session, Any, Any]:
    db = Database(cfg.get_db_addr())
    yield from db.get_db()


_task_storage: Dict[int, Task] = {}
_user_storage: Dict[int, User] = {}


def get_in_memory_task_repository() -> ITaskRepository:
    return InMemoryTaskRepository(_task_storage)


def get_in_memory_user_repository() -> IUserRepository:
    return InMemoryUserRepository(_user_storage)


def get_postgres_user_repository(db: Session) -> IUserRepository:
    return PostgreSQLUserRepository(db)


def get_postgres_task_repository(db: Session) -> ITaskRepository:
    return PostgreSQLTaskRepository(db)


def get_task_repository(cfg: Config = Depends(get_config)) -> ITaskRepository:
    if cfg.env == "prod":
        db = get_db(cfg)
        session = next(db)
        return get_postgres_task_repository(session)
    return get_in_memory_task_repository()


def get_user_repository(cfg: Config = Depends(get_config)) -> IUserRepository:
    if cfg.env == "prod":
        db = get_db(cfg)
        session = next(db)
        return get_postgres_user_repository(session)
    return get_in_memory_user_repository()


def get_task_service(
    repo: ITaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repo)


def get_user_service(
    repo: IUserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)
