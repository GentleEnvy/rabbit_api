from django.db import models

from api.models import Rabbit
from api.models.base import BaseHistoryModel

__all__ = ['RabbitHistory']


class RabbitHistory(BaseHistoryModel):
    historical_pk_name = 'rabbit'

    rabbit = models.OneToOneField(Rabbit, on_delete=models.CASCADE)
    is_vaccinated = models.BooleanField(null=True, blank=True)
    is_ill = models.BooleanField(null=True, blank=True)
    current_type = models.CharField(max_length=1)
