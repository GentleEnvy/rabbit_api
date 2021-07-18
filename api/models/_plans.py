from django.db import models
from django.utils import timezone

from api.models.base import BaseModel

__all__ = ['Plan']


# TODO: add validation:
#   - fatteningrabbit_set.count() <= quantity
class Plan(BaseModel):
    date = models.DateField(default=timezone.now)
    quantity = models.PositiveSmallIntegerField()
