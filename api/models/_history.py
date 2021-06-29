from django.db import models

from api.models.base import BaseHistoryModel

__all__ = ['RabbitHistory']


class RabbitHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'
    historical_pk_name = 'rabbit'

    rabbit = models.ForeignKey(historical_name.title(), on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    is_vaccinated = models.BooleanField(null=True, blank=True)
    is_ill = models.BooleanField(null=True, blank=True)
    current_type = models.CharField(max_length=1)
