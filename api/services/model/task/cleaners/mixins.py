from typing import Type

from api.services.model.task.cleaners._cleaner import *

__all__ = [
    'TaskCleanerMixin', 'ToReproductionTaskCleanerMixin', 'ToFatteningTaskCleanerMixin',
    'MatingTaskCleanerMixin', 'BunnyJiggingTaskCleanerMixin',
    'VaccinationTaskCleanerMixin', 'SlaughterInspectionTaskCleanerMixin',
    'SlaughterTaskCleanerMixin'
]


class TaskCleanerMixin:
    Cleaner: Type[TaskCleaner] = TaskCleaner
    
    @property
    def cleaner(self) -> TaskCleaner:
        return self.Cleaner(self)
    
    def clean(self):
        # noinspection PyUnresolvedReferences
        super().clean()
        self.cleaner.clean()


class ToReproductionTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = ToReproductionTaskCleaner
    
    @property
    def cleaner(self) -> ToReproductionTaskCleaner:
        return self.Cleaner(self)


class ToFatteningTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = ToFatteningTaskCleaner
    
    @property
    def cleaner(self) -> ToFatteningTaskCleaner:
        return self.Cleaner(self)


class MatingTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = MatingTaskCleaner
    
    @property
    def cleaner(self) -> MatingTaskCleaner:
        return self.Cleaner(self)


class BunnyJiggingTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = BunnyJiggingTaskCleaner
    
    @property
    def cleaner(self) -> BunnyJiggingTaskCleaner:
        return self.Cleaner(self)


class VaccinationTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = VaccinationTaskCleaner
    
    @property
    def cleaner(self) -> VaccinationTaskCleaner:
        return self.Cleaner(self)


class SlaughterInspectionTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = SlaughterTaskCleaner
    
    @property
    def cleaner(self) -> SlaughterTaskCleaner:
        return self.Cleaner(self)


class SlaughterTaskCleanerMixin(TaskCleanerMixin):
    Cleaner = SlaughterTaskCleaner
    
    @property
    def cleaner(self) -> SlaughterTaskCleaner:
        return self.Cleaner(self)
