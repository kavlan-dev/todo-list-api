from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from todo_list_api.depends import get_jwt_auth, get_user_service
from todo_list_api.models.user import UserCreate, UserLogin, UserResponse
from todo_list_api.services.user import UserService
from todo_list_api.utils.security import JWTAuth


router = APIRouter(prefix="/api/users")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    new_user: UserCreate, service: UserService = Depends(get_user_service)
):
    user = service.register_user(new_user)
    if user:
        return user
    return JSONResponse(
        {"error": "Не удалось зарегестрировать пользователя"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    user_login: UserLogin,
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
    service: UserService = Depends(get_user_service),
):
    user = service.login_user(user_login)
    if user:
        token = jwt_auth.create_jwt_token(
            {"username": user.username, "user_id": user.id}
        )
        return {"access_token": token, "token_type": "bearer"}
    return JSONResponse(
        {"error": "не верные данные"}, status_code=status.HTTP_400_BAD_REQUEST
    )
