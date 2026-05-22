from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.orm import Session
from todo_list_api.models.user import User, UserModel


class IUserRepository(ABC):
    @abstractmethod
    def create(self, new_user: User) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass


class InMemoryUserRepository(IUserRepository):
    def __init__(self, storage: Dict[int, User]) -> None:
        self._users = storage

    def _generate_id(self) -> int:
        if not self._users:
            return 1

        return max(i for i in self._users) + 1

    def _get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user

    def create(self, new_user: User) -> User:
        existing_user_by_username = self.get_by_username(new_user.username)
        if existing_user_by_username:
            raise ValueError(
                f"Пользователь с именем '{new_user.username}' уже существует"
            )

        existing_user_by_email = self._get_by_email(new_user.email)
        if existing_user_by_email:
            raise ValueError(f"Пользователь с email '{new_user.email}' уже существует")

        uid = self._generate_id()
        now = datetime.now()

        new_user.id = uid
        new_user.created_at = now
        new_user.updated_at = now

        self._users[uid] = new_user
        return new_user

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user


class PostgreSQLUserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, new_user: User) -> User:
        user_model = UserModel(**new_user.model_dump())
        self._session.add(user_model)
        self._session.commit()
        self._session.refresh(user_model)
        return User.model_validate(vars(user_model))

    def get_by_username(self, username: str) -> Optional[User]:
        user_model = (
            self._session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        if user_model:
            return User.model_validate(vars(user_model))
        return None
