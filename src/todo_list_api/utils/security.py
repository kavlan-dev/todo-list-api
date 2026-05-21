from datetime import datetime, timedelta
from typing import Dict

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

auth_scheme = HTTPBearer()


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class JWTAuth:
    def __init__(self, secret_key: str) -> None:
        self._secret_key = secret_key
        self._access_token_expire = 30
        self._algorithm = "HS256"

    def create_jwt_token(self, data: Dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self._access_token_expire)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def get_user_from_token(
        self, token: HTTPAuthorizationCredentials = Depends(auth_scheme)
    ):
        payload = jwt.decode(
            token.credentials, self._secret_key, algorithms=[self._algorithm]
        )
        return payload
