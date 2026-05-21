from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials

from todo_list_api.depends import get_jwt_auth, get_task_service
from todo_list_api.models.task import TaskCreate, TaskResponse, TaskUpdate
from todo_list_api.services.task import TaskService
from todo_list_api.utils.security import JWTAuth, auth_scheme

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def create_task(
    new_task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
):
    user_id = int(jwt_auth.get_user_from_token(token)["user_id"])
    task = service.create_task(new_task, user_id)
    if task:
        return task
    return JSONResponse(
        {"error": "не удалось создать задачу"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(
    service: TaskService = Depends(get_task_service),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
):
    user_id = int(jwt_auth.get_user_from_token(token)["user_id"])
    task = service.get_all_tasks(user_id)
    if task:
        return task
    return JSONResponse({"message": "нет задач"}, status_code=status.HTTP_200_OK)


@router.get("/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(
    id: int,
    service: TaskService = Depends(get_task_service),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
):
    user_id = int(jwt_auth.get_user_from_token(token)["user_id"])
    task = service.get_task_by_id(id, user_id)
    if task:
        return task
    return JSONResponse(
        {"message": "задача не найдена"}, status_code=status.HTTP_404_NOT_FOUND
    )


@router.put("/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
):
    user_id = int(jwt_auth.get_user_from_token(token)["user_id"])
    task = service.update_task(id, task_update, user_id)
    if task:
        return task
    return JSONResponse(
        {"message": "задача не найдена"}, status_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    service: TaskService = Depends(get_task_service),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_auth: JWTAuth = Depends(get_jwt_auth),
):
    user_id = int(jwt_auth.get_user_from_token(token)["user_id"])
    ok = service.delete_task(id, user_id)
    if ok:
        return
    return JSONResponse(
        {"message": "задача не найдена"}, status_code=status.HTTP_404_NOT_FOUND
    )
