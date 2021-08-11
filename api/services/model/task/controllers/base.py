from abc import ABC
from typing import final, Type

from django.core.exceptions import ValidationError
from model_utils.managers import InheritanceQuerySet

from api.models import Task

__all__ = ['TaskController']


class TaskController(ABC):
    task_model: Type[Task] = Task
    
    @final
    def update_anonymous(self) -> None:
        self._clear(self.anonymous | self.in_progress)
        self._create(self.anonymous | self.in_progress | self.waiting_confirmation)
    
    @final
    def update_in_progress(self) -> None:
        self._setup(self.in_progress)
    
    @property
    def anonymous(self) -> InheritanceQuerySet:
        return self.task_model.objects.select_subclasses().filter(user=None)
    
    @property
    def in_progress(self) -> InheritanceQuerySet:
        return self.task_model.objects.select_subclasses().exclude(user=None).filter(
            completed_at=None
        )
    
    @property
    def waiting_confirmation(self) -> InheritanceQuerySet:
        return self.task_model.objects.select_subclasses().exclude(
            completed_at=None
        ).filter(is_confirmed=None)
    
    @staticmethod
    def _clear(tasks: InheritanceQuerySet) -> None:
        for task in tasks.all():
            try:
                task.full_clean()
            except ValidationError:
                task.delete()
    
    def _create(self, tasks: InheritanceQuerySet) -> None:
        pass
    
    def _setup(self, tasks: InheritanceQuerySet) -> None:
        pass
    
    def execute(self, task: Task) -> None:
        raise NotImplementedError
