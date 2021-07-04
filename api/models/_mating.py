from django.db import models
from django.utils import timezone

from api.models.base import BaseModel

__all__ = ['Mating']


class Mating(BaseModel):
    time = models.DateTimeField(default=timezone.now)
    mother_rabbit = models.ForeignKey('MotherRabbit', on_delete=models.CASCADE)
    father_rabbit = models.ForeignKey('FatherRabbit', on_delete=models.CASCADE)
