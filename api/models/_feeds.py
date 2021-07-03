from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from api.models.base import BaseModel

__all__ = ['FeedBatch']


class FeedBatch(BaseModel):
    delivery_date = models.DateField(default=now)
    bags_number = models.IntegerField(null=False, blank=False)

    def clean(self):
        super().clean()
        if self.delivery_date > now():
            raise ValidationError('Wrong date of delivery input')
