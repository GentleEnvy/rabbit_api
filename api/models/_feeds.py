from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

from api.models.base import BaseModel

__all__ = ['FeedBatch']


class FeedBatch(BaseModel):
    delivery_date = models.DateField(default=date.today())
    total_bags_number = models.IntegerField(null=False, blank=False)
    bags_left = models.IntegerField(null=False, blank=False)

    def clean(self):
        super().clean()
        if self.delivery_date > date.today():
            raise ValidationError('Wrong date of delivery input')
