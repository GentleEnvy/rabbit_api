from abc import ABC
from typing import final, Type

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from api.models import Task

__all__ = ['BaseTaskController']


class BaseTaskController(ABC):
    task_model: Type[Task]
    
    @final
    def update(self) -> None:
        self._clear(self.anonymous | self.in_progress)
        self._create(self.anonymous | self.in_progress | self.waiting_confirmation)
        self._setup(self.in_progress)
    
    @property
    def anonymous(self) -> QuerySet:
        return self.task_model.objects.filter(user=None)
    
    @property
    def in_progress(self) -> QuerySet:
        return self.task_model.objects.exclude(user=None).filter(completed_at=None)
    
    @property
    def waiting_confirmation(self) -> QuerySet:
        return self.task_model.objects.exclude(completed_at=None).filter(
            is_confirmed=None
        )
    
    @staticmethod
    def _clear(tasks: QuerySet) -> None:
        for task in tasks.all():
            try:
                task.full_clean()
            except ValidationError:
                task.delete()
    
    def _create(self, tasks: QuerySet) -> None:
        pass
    
    def _setup(self, tasks: QuerySet) -> None:
        pass
