from django.db import models
from django.utils import timezone

from api.models.base import BaseModel

__all__ = ['Plan']


class Plan(BaseModel):
    type = models.CharField(
        choices=(
            (SLAUGHTER := 'S', 'SLAUGHTER'),
            (MATING := 'M', 'MATING')
        ),
        max_length=1
    )
    date = models.DateField(default=timezone.now)
    quantity = models.PositiveSmallIntegerField()
    is_completed = models.BooleanField(default=False)
