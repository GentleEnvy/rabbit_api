from __future__ import annotations

from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.db import models

from api.models.base import BaseModel

__all__ = ['CommonFeeds', 'NursingMotherFeeds']


class CommonFeeds(BaseModel):
    date = models.DateField(default=datetime.utcnow)
    stocks_change = models.IntegerField(default=0)
    
    def clean(self):
        super().clean()
        if self.date > date.today():
            raise ValidationError('Wrong date of common feeds stocks change input')


class NursingMotherFeeds(BaseModel):
    date = models.DateField(default=datetime.utcnow)
    stocks_change = models.IntegerField(default=0)
    
    def clean(self):
        super().clean()
        if self.date > date.today():
            raise ValidationError('Wrong date of mother feeds stocks change input')
