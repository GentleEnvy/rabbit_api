from datetime import datetime

from django.db import models

from api.models.base import BaseModel

__all__ = ['Plan']


# TODO: add validation:
#   - fatteningrabbit_set.count() <= quantity
class Plan(BaseModel):
    date = models.DateField(default=datetime.utcnow)
    quantity = models.PositiveSmallIntegerField()
