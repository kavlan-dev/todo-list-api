from typing import List, Optional

from todo_list_api.models.task import Task, TaskCreate, TaskUpdate
from todo_list_api.repositories.task import ITaskRepository


class TaskService:
    def __init__(self, repo: ITaskRepository) -> None:
        self._repo = repo

    def create_task(self, new_task: TaskCreate, user_id: int) -> Task:
        return self._repo.create(new_task, user_id)

    def get_all_tasks(self, user_id: int) -> List[Task]:
        tasks = self._repo.get_all()
        user_tasks = []
        for task in tasks:
            if task and int(str(task.user_id)) == user_id:
                user_tasks.append(task)
        return user_tasks

    def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        task = self._repo.get_by_id(task_id)
        if task and int(str(task.user_id)) == user_id:
            return task

    def update_task(
        self, task_id: int, task_update: TaskUpdate, user_id: int
    ) -> Optional[Task]:
        task = self._repo.get_by_id(task_id)
        if task and int(str(task.user_id)) == user_id:
            return self._repo.update(task_id, task_update)

    def delete_task(self, task_id: int, user_id: int) -> bool:
        task = self._repo.get_by_id(task_id)
        if task and int(str(task.user_id)) == user_id:
            return self._repo.delete(task_id)
        return False
