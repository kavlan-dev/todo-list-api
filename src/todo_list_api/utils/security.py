from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends

auth_scheme = HTTPBearer()


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
