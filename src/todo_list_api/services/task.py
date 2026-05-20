from typing import List, Optional

from todo_list_api.models.task import Task, TaskCreate, TaskUpdate
from todo_list_api.repositories.task import ITaskRepository


class TaskService:
    def __init__(self, repo: ITaskRepository) -> None:
        self._repo = repo

    def create_task(self, task_data: TaskCreate) -> Task:
        return self._repo.create(task_data)

    def get_task_by_id(self, id: int) -> Optional[Task]:
        return self._repo.get_by_id(id)

    def get_all_tasks(self) -> List[Task]:
        return self._repo.get_all()

    def update_task(self, id: int, task_data: TaskUpdate) -> Optional[Task]:
        return self._repo.update(id, task_data)

    def delete_task(self, id: int) -> bool:
        return self._repo.delete(id)
