from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

from django.utils import timezone

from api.models.base import BaseModel

__all__ = ['FeedBatch']


class FeedBatch(BaseModel):
    delivery_date = models.DateField(default=timezone.now)
    total_common_bags_number = models.IntegerField(default=0)
    common_bags_left = models.IntegerField(default=0)
    total_mother_bags_number = models.IntegerField(default=0)
    mother_bags_left = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.delivery_date > date.today():
            raise ValidationError('Wrong date of delivery input')
