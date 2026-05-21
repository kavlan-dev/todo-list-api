from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from todo_list_api.models.task import Task, TaskCreate, TaskUpdate


class ITaskRepository(ABC):
    @abstractmethod
    def create(self, new_task: TaskCreate, user_id: int) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, id: int, task_update: TaskUpdate) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}

    def _generate_id(self) -> int:
        if not self._tasks:
            return 1

        return max(i for i in self._tasks) + 1

    def create(self, new_task: TaskCreate, user_id: int) -> Task:
        tid = self._generate_id()
        task = Task(
            id=tid,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **new_task.model_dump(),
        )
        self._tasks[tid] = task
        return task

    def get_all(self) -> List[Task]:
        return list(self._tasks.values())

    def get_by_id(self, id: int) -> Optional[Task]:
        return self._tasks.get(id, None)

    def update(self, id: int, task_update: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(id)
        if task:
            update_data = task_update.model_dump(exclude_unset=False)
            for key, value in update_data.items():
                setattr(task, key, value)
            return task
        return None

    def delete(self, id: int) -> bool:
        return True if self._tasks.pop(id, None) else False
