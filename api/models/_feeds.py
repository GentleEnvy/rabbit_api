from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from api.models.base import BaseModel

__all__ = ['Feeds', 'FatteningFeeds', 'MotherFeeds']


def _stocks_validator(stocks):
    if stocks == 0:
        raise ValidationError('Stocks cannot be zero', code='value')


class Feeds(BaseModel):
    time = models.DateTimeField(default=datetime.utcnow)
    stocks = models.SmallIntegerField(validators=[_stocks_validator])


class FatteningFeeds(Feeds):
    pass


class MotherFeeds(Feeds):
    pass
