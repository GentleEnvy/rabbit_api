from datetime import datetime

from django.db import models

from api.models.base import BaseModel

__all__ = ['Mating']


class Mating(BaseModel):
    time = models.DateTimeField(default=datetime.utcnow)
    mother_rabbit = models.ForeignKey('MotherRabbit', on_delete=models.CASCADE)
    father_rabbit = models.ForeignKey('FatherRabbit', on_delete=models.CASCADE)
