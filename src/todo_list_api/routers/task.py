import logging

from fastapi import APIRouter, Depends, status

from todo_list_api.depends import get_logger, get_service
from todo_list_api.models.task import TaskCreate, TaskResponse
from todo_list_api.services.task import TaskService

router = APIRouter(prefix="/api/tasks")


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_service),
    log: logging.Logger = Depends(get_logger),
):
    task = service.create_task(task_data)
    if task:
        log.info(f"Добавлена новая задача (ID: {task.id})")
        return task
    log.error(f"Не удалось создать задачу {task_data}")
