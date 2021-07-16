from django.db import models
from django.utils import timezone

from api.models._rabbits import *
from api.models.base import BaseModel

__all__ = ['Task', 'SlaughterTask', 'MatingTask']


class Task(BaseModel):
    date = models.DateField(default=timezone.now)


class SlaughterTask(Task):
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.PROTECT)


class MatingTask(Task):
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.PROTECT)
    father_rabbit = models.ForeignKey(FatherRabbit, on_delete=models.PROTECT)
