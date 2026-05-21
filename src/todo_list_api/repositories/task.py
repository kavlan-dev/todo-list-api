from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from todo_list_api.models.task import Task, TaskModel


class ITaskRepository(ABC):
    @abstractmethod
    def create(self, new_task: Task) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, id: int, task_update: Task) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self, storage: Dict[int, Task]) -> None:
        self._tasks = storage

    def _generate_id(self) -> int:
        if not self._tasks:
            return 1

        return max(i for i in self._tasks) + 1

    def create(self, new_task: Task) -> Task:
        tid = self._generate_id()
        now = datetime.now()

        new_task.id = tid
        new_task.created_at = now
        new_task.updated_at = now

        self._tasks[tid] = new_task
        return new_task

    def get_all(self) -> List[Task]:
        return list(self._tasks.values())

    def get_by_id(self, id: int) -> Optional[Task]:
        return self._tasks.get(id, None)

    def update(self, id: int, task_update: Task) -> Optional[Task]:
        task = self.get_by_id(id)
        if task:
            for key, value in vars(task_update).items():
                if value is not None:
                    setattr(task, key, value)
            task.updated_at = datetime.now()
            return task

    def delete(self, id: int) -> bool:
        return True if self._tasks.pop(id, None) else False


class PostgreSQLTaskRepository(ITaskRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, new_task: Task) -> Task:
        task_model = TaskModel(**new_task.model_dump())
        self._session.add(task_model)
        self._session.commit()
        self._session.refresh(task_model)
        return Task.model_validate(vars(task_model))

    def get_all(self) -> List[Task]:
        task_models = self._session.query(TaskModel).all()
        return [Task.model_validate(vars(task_model)) for task_model in task_models]

    def get_by_id(self, id: int) -> Optional[Task]:
        task_model = self._session.query(TaskModel).filter(TaskModel.id == id).first()
        if task_model:
            return Task.model_validate(vars(task_model))
        return None

    def update(self, id: int, task_update: Task) -> Optional[Task]:
        task_model = self._session.query(TaskModel).filter(TaskModel.id == id).first()
        if task_model:
            update_data = task_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task_model, key, value)
            self._session.commit()
            self._session.refresh(task_model)
            return Task.model_validate(vars(task_model))
        return None

    def delete(self, id: int) -> bool:
        task_model = self._session.query(TaskModel).filter(TaskModel.id == id).first()
        if task_model:
            self._session.delete(task_model)
            self._session.commit()
            return True
        return False
