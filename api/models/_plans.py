from django.db import models
from django.utils import timezone

from api.models.base import BaseModel

__all__ = ['Plan', 'SlaughterPlan', 'MatingPlan']


class Plan(BaseModel):
    date = models.DateField(default=timezone.now)
    is_completed = models.BooleanField(default=False)


class SlaughterPlan(Plan):
    number_rabbits = models.PositiveSmallIntegerField()


class MatingPlan(Plan):
    number_pairs = models.PositiveSmallIntegerField()
