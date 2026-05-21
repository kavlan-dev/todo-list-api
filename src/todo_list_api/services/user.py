from typing import Optional

from todo_list_api.models.user import User, UserCreate, UserLogin
from todo_list_api.repositories.user import IUserRepository
from todo_list_api.utils.security import PasswordHasher


class UserService:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    def register_user(self, new_user: UserCreate) -> User:
        hashed_pass = PasswordHasher.hash_password(new_user.password)
        user_data = new_user.model_dump()
        user = User(
            id=None,
            created_at=None,
            updated_at=None,
            password_hash=hashed_pass,
            **user_data,
        )
        return self._repo.create(user)

    def login_user(self, user_login: UserLogin) -> Optional[User]:
        user = self._repo.get_by_username(user_login.username)
        if user and PasswordHasher.verify_password(
            user_login.password, user.password_hash
        ):
            return user
        return
