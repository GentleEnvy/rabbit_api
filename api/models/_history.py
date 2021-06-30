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


class RabbitHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit = models.ForeignKey('Rabbit', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    is_vaccinated = models.BooleanField(**_field_kwargs)
    is_ill = models.BooleanField(**_field_kwargs)
    current_type = models.TextField(**_field_kwargs)


class FatteningRabbitHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit = models.ForeignKey('FatteningRabbit', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    cage = models.IntegerField(**_field_kwargs)


class BunnyHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit = models.ForeignKey('Bunny', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    need_jigging = models.BooleanField(**_field_kwargs)
    cage = models.IntegerField(**_field_kwargs)


class MotherRabbitHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit = models.ForeignKey('MotherRabbit', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    status = models.TextField(**_field_kwargs)
    last_childbirth = models.DateField(**_field_kwargs)
    cage = models.IntegerField(**_field_kwargs)


class FatherRabbitHistory(BaseHistoryModel):
    class Meta:
        unique_together = ('rabbit', 'time')

    historical_name = 'rabbit'

    rabbit = models.ForeignKey('FatherRabbit', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    is_resting = models.BooleanField(**_field_kwargs)
    cage = models.IntegerField(**_field_kwargs)
