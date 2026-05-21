from typing import Optional
from todo_list_api.models.user import User, UserCreate, UserLogin
from todo_list_api.repositories.user import IUserRepository


class UserService:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    def register_user(self, new_user: UserCreate) -> User:
        return self._repo.create(new_user)

    def login_user(self, user_login: UserLogin) -> Optional[User]:
        user = self._repo.get_by_username(user_login.username)
        if user and str(user.password_hash) == user_login.password:
            return user
        return
