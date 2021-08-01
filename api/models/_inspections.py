from datetime import datetime

from django.db import models

from api.models._rabbits import *
from api.models.base import *

__all__ = ['PregnancyInspection']


class PregnancyInspection(BaseModel):
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.utcnow)
    is_pregnant = models.BooleanField()
