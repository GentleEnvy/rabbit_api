from datetime import datetime

from django.db import models

from api.models._rabbits import *
from api.models.base import *

__all__ = ['BeforeSlaughterInspection', 'PregnancyInspection']


class BeforeSlaughterInspection(BaseModel):
    rabbit = models.ForeignKey(Rabbit, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.utcnow)
    delay = models.IntegerField(null=True, blank=True)  # TODO: not null


class PregnancyInspection(BaseModel):
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.utcnow)
    is_pregnant = models.BooleanField()
