import os
from typing import Any, Generator, Optional

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session

from todo_list_api.config import Config, DBConfig
from todo_list_api.db import Database
from todo_list_api.repositories.task import InMemoryTaskRepository, ITaskRepository
from todo_list_api.repositories.user import IUserRepository, InMemoryUserRepository
from todo_list_api.services.task import TaskService
from todo_list_api.services.user import UserService
from todo_list_api.utils.security import JWTAuth


def get_config() -> Config:
    load_dotenv()
    cfg = Config(
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", ""),
        env=os.getenv("ENV", "local"),
        db_cfg=DBConfig(
            user=os.getenv("POSTGRES_USER", ""),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            name=os.getenv("POSTGRES_DB", ""),
        ),
    )
    return cfg


def get_jwt_auth(cfg: Config = Depends(get_config)) -> JWTAuth:
    return JWTAuth(cfg.jwt_secret_key)


def get_db(cfg: Config) -> Generator[Session, Any, Any]:
    db = Database(cfg.get_db_addr())
    yield from db.get_db()


_task_repo: Optional[ITaskRepository] = None
_user_repo: Optional[IUserRepository] = None


def get_in_memory_task_repository() -> ITaskRepository:
    global _task_repo
    if not _task_repo:
        _task_repo = InMemoryTaskRepository()
    return _task_repo


def get_in_memory_user_repository() -> IUserRepository:
    global _user_repo
    if not _user_repo:
        _user_repo = InMemoryUserRepository()
    return _user_repo


def get_task_repository(cfg: Config = Depends(get_config)) -> ITaskRepository:
    # if cfg.env == "prod":
    #     db = get_db(cfg)
    #     session = next(db)
    #     return get_postgres_repository(session)
    return get_in_memory_task_repository()


def get_user_repository(cfg: Config = Depends(get_config)) -> IUserRepository:
    return get_in_memory_user_repository()


def get_task_service(
    repo: ITaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repo)


def get_user_service(
    repo: IUserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)
