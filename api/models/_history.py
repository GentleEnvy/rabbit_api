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
    historical_name = 'rabbit'
    replace_fields = {'cage': 'cage_id'}

    time = models.DateTimeField(auto_now_add=True)

    is_vaccinated = models.BooleanField(**_field_kwargs)
    current_type = models.TextField(**_field_kwargs)
    warning_status = models.TextField(**_field_kwargs)


class FatteningRabbitHistory(RabbitHistory):
    rabbit = models.ForeignKey('FatteningRabbit', on_delete=models.CASCADE)

    cage = models.ForeignKey(
        'FatteningCage', on_delete=models.DO_NOTHING, **_field_kwargs
    )


class BunnyHistory(RabbitHistory):
    rabbit = models.ForeignKey('Bunny', on_delete=models.CASCADE)

    cage = models.ForeignKey('MotherCage', on_delete=models.DO_NOTHING, **_field_kwargs)


class MotherRabbitHistory(RabbitHistory):
    rabbit = models.ForeignKey('MotherRabbit', on_delete=models.CASCADE)

    cage = models.ForeignKey('MotherCage', on_delete=models.DO_NOTHING, **_field_kwargs)


class FatherRabbitHistory(RabbitHistory):
    rabbit = models.ForeignKey('FatherRabbit', on_delete=models.CASCADE)

    cage = models.ForeignKey(
        'FatteningCage', on_delete=models.DO_NOTHING, **_field_kwargs
    )
