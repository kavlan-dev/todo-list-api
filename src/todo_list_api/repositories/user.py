from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional

from todo_list_api.models.user import User, UserCreate


class IUserRepository(ABC):
    @abstractmethod
    def create(self, new_user: UserCreate) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass


class InMemoryUserRepository(IUserRepository):
    def __init__(self) -> None:
        self._users: Dict[int, User] = {}

    def _generate_id(self) -> int:
        if not self._users:
            return 1

        return max(i for i in self._users) + 1

    def create(self, new_user: UserCreate) -> User:
        uid = self._generate_id()
        user = User(
            id=uid,
            username=new_user.username,
            email=new_user.email,
            password_hash=new_user.password,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._users[uid] = user
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if str(user.username) == username:
                return user
        return None
