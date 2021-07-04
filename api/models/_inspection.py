from django.db import models
from django.utils import timezone

from api.models._rabbits import *
from api.models.base import *

__all__ = ['Inspection']


class Inspection(BaseModel):
    rabbit = models.ForeignKey(Rabbit, on_delete=models.CASCADE)
    time = models.DateField(default=timezone.now)
    weight = models.FloatField()
    delay = models.IntegerField(null=True, blank=True)
