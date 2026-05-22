from typing import List, Optional

from todo_list_api.models.task import Task, TaskCreate, TaskUpdate
from todo_list_api.repositories.task import ITaskRepository


class TaskService:
    def __init__(self, repo: ITaskRepository) -> None:
        self._repo = repo

    def create_task(self, user_id: int, new_task: TaskCreate) -> Task:
        task = Task(
            id=None,
            created_at=None,
            updated_at=None,
            user_id=None,
            **new_task.model_dump(),
        )
        return self._repo.create(user_id, task)

    def get_all_tasks(self, user_id: int, page: int, limit: int) -> List[Task]:
        return self._repo.get_all(user_id, page, limit)

    def get_task_by_id(self, user_id: int, task_id: int) -> Optional[Task]:
        return self._repo.get_by_id(user_id, task_id)

    def update_task(
        self, user_id: int, task_id: int, task_update: TaskUpdate
    ) -> Optional[Task]:
        task = Task(
            id=None,
            created_at=None,
            updated_at=None,
            user_id=None,
            **task_update.model_dump(),
        )
        return self._repo.update(user_id, task_id, task)

    def delete_task(self, user_id: int, task_id: int) -> bool:
        return self._repo.delete(user_id, task_id)
