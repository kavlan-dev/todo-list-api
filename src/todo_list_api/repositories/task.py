from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from todo_list_api.models.task import Task, TaskCreate, TaskUpdate


class ITaskRepository(ABC):
    @abstractmethod
    def create(self, task_data: TaskCreate) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, id: int, task_data: TaskUpdate) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self) -> None:
        self._task: Dict[int, Task] = {}

    def _generate_id(self) -> int:
        if not self._task:
            return 1

        return max(i for i in self._task) + 1

    def create(self, task_data: TaskCreate) -> Task:
        tid = self._generate_id()
        task = Task(
            id=tid,
            user_id=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **task_data.model_dump(),
        )
        self._task[tid] = task
        return task

    def get_all(self) -> List[Task]:
        return list(self._task.values())

    def get_by_id(self, id: int) -> Optional[Task]:
        return self._task.get(id, None)

    def update(self, id: int, task_data: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(id)
        if task:
            update_data = task_data.model_dump(exclude_unset=False)
            for key, value in update_data.items():
                setattr(task, key, value)
            return task
        return None

    def delete(self, id: int) -> bool:
        return True if self._task.pop(id, None) else False
