from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils.managers import InheritanceManager
from simple_history.models import HistoricalRecords

from api.models._cages import *
from api.models._rabbits import *
from api.models.base import BaseModel
from api.services.model.task.cleaners.mixins import *

__all__ = [
    'Task', 'ToReproductionTask', 'ToFatteningTask', 'MatingTask', 'BunnyJiggingTask',
    'VaccinationTask', 'SlaughterInspectionTask', 'SlaughterTask'
]


class Task(TaskCleanerMixin, BaseModel):
    objects = InheritanceManager()
    
    CHAR_TYPE: str
    
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)


class ToReproductionTask(ToReproductionTaskCleanerMixin, Task):
    CHAR_TYPE = 'R'
    history = HistoricalRecords()
    
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.CASCADE)
    # in progress
    cage_to = models.ForeignKey(Cage, on_delete=models.CASCADE, null=True, blank=True)


class ToFatteningTask(ToFatteningTaskCleanerMixin, Task):
    CHAR_TYPE = 'F'
    history = HistoricalRecords()
    
    rabbit = models.ForeignKey(Rabbit, on_delete=models.CASCADE)
    # in progress
    cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE, null=True, blank=True
    )


class MatingTask(MatingTaskCleanerMixin, Task):
    CHAR_TYPE = 'M'
    history = HistoricalRecords()
    
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.CASCADE)
    father_rabbit = models.ForeignKey(FatherRabbit, on_delete=models.CASCADE)


# noinspection SpellCheckingInspection
class BunnyJiggingTask(BunnyJiggingTaskCleanerMixin, Task):
    CHAR_TYPE = 'B'
    history = HistoricalRecords()
    
    cage_from = models.ForeignKey(MotherCage, on_delete=models.CASCADE)
    # in progress
    male_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_male_set'
    )
    female_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_female_set'
    )
    males = models.PositiveSmallIntegerField(null=True, blank=True)


class VaccinationTask(VaccinationTaskCleanerMixin, Task):
    CHAR_TYPE = 'V'
    history = HistoricalRecords()
    
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)


class SlaughterInspectionTask(SlaughterInspectionTaskCleanerMixin, Task):
    CHAR_TYPE = 'I'
    history = HistoricalRecords()
    
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)
    # in progress
    weights: list[float] = ArrayField(models.FloatField(), null=True, blank=True)


class SlaughterTask(SlaughterTaskCleanerMixin, Task):
    CHAR_TYPE = 'S'
    history = HistoricalRecords()
    
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.CASCADE)
