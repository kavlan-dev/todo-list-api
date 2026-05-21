from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from todo_list_api.models.user import Base


class Database:
    def __init__(self, db_url: str):
        self.DATABASE_URL = db_url
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Generator[Session, Any, Any]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
