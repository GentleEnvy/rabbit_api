from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from api.models.base import BaseModel

__all__ = ['Plan']


class Plan(BaseModel):
    date = models.DateField(default=datetime.utcnow)
    quantity = models.PositiveSmallIntegerField()
    
    def clean(self):
        if self.fatteningrabbit_set.count() > self.quantity:
            raise ValidationError(
                'The number of rabbits in the plan exceeds the required quantity'
            )
