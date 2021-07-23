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
        self._clear()
        self._create()
        self._update()
    
    @property
    def anonymous(self) -> QuerySet:
        return self.task_model.objects.filter(user=None)
    
    @property
    def completed(self) -> QuerySet:
        return self.task_model.objects.exclude(completed_at=None)
    
    @property
    def uncompleted(self) -> QuerySet:
        return self.task_model.objects.filter(completed_at=None)
    
    @property
    def waiting_confirmation(self) -> QuerySet:
        return self.task_model.objects.filter(is_confirmed=None)
    
    @property
    def confirmed(self) -> QuerySet:
        return self.task_model.objects.filter(is_confirmed=True)
    
    @property
    def unconfirmed(self) -> QuerySet:
        return self.task_model.objects.filter(is_confirmed=False)
    
    def _clear(self) -> None:
        for task in self.uncompleted.all():
            try:
                task.full_clean()
            except ValidationError:
                task.delete()
    
    def _create(self) -> None:
        pass
    
    def _update(self) -> None:
        pass
