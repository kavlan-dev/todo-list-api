import logging
import os
from typing import Any, Generator, Optional

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session

from todo_list_api.config import Config, DBConfig
from todo_list_api.db import Database
from todo_list_api.repositories.task import InMemoryTaskRepository, ITaskRepository
from todo_list_api.services.task import TaskService
from todo_list_api.utils.logger import setup_logger


def get_config() -> Config:
    load_dotenv()
    cfg = Config(
        env=os.getenv("ENV", "local"),
        db_cfg=DBConfig(
            user=os.getenv("POSTGRES_USER", ""),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            name=os.getenv("POSTGRES_DB", ""),
        ),
    )
    return cfg


def get_logger() -> logging.Logger:
    return setup_logger()


def get_db(cfg: Config) -> Generator[Session, Any, Any]:
    db = Database(cfg.get_db_addr())
    yield from db.get_db()


_db: Optional[ITaskRepository] = None


def get_in_memory_repository() -> ITaskRepository:
    global _db
    if not _db:
        _db = InMemoryTaskRepository()
    return _db


def get_repository(cfg: Config = Depends(get_config)) -> ITaskRepository:
    # if cfg.env == "prod":
    #     db = get_db(cfg)
    #     session = next(db)
    #     return get_postgres_repository(session)
    return get_in_memory_repository()


def get_service(
    repo: ITaskRepository = Depends(get_repository),
) -> TaskService:
    return TaskService(repo)
