from django.db import models

from api.models.base import BaseHistoryModel

__all__ = [
    'RabbitHistory', 'FatteningRabbitHistory', 'BunnyHistory', 'MotherRabbitHistory',
    'FatherRabbitHistory'
]

_field_kwargs = {
    'null': True,
    'blank': True,
    'default': None
}


class _BaseRabbitHistory(BaseHistoryModel):
    class Meta:
        abstract = True
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit: models.ForeignKey
    time = models.DateTimeField(auto_now_add=True)


class RabbitHistory(_BaseRabbitHistory):
    rabbit = models.ForeignKey('Rabbit', on_delete=models.CASCADE)

    is_vaccinated = models.BooleanField(**_field_kwargs)
    current_type = models.TextField(**_field_kwargs)
    warning_status = models.TextField(**_field_kwargs)


class FatteningRabbitHistory(_BaseRabbitHistory):
    rabbit = models.ForeignKey('FatteningRabbit', on_delete=models.CASCADE)

    cage = models.IntegerField(**_field_kwargs)


class BunnyHistory(_BaseRabbitHistory):
    rabbit = models.ForeignKey('Bunny', on_delete=models.CASCADE)

    cage = models.IntegerField(**_field_kwargs)


class MotherRabbitHistory(_BaseRabbitHistory):
    rabbit = models.ForeignKey('MotherRabbit', on_delete=models.CASCADE)

    cage = models.IntegerField(**_field_kwargs)
    is_pregnant = models.BooleanField(**_field_kwargs)


class FatherRabbitHistory(_BaseRabbitHistory):
    rabbit = models.ForeignKey('FatherRabbit', on_delete=models.CASCADE)

    cage = models.IntegerField(**_field_kwargs)
