from django.db import models
from multiselectfield import MultiSelectField

from api.models._cages import BaseCage, FatteningCage, MotherCage

__all__ = ['BaseCage', 'FatteningRabbit', 'Bunny', 'MotherRabbit', 'FatherRabbit']

_is_valid_cage = {'status': []}


class BaseRabbit(models.Model):
    birthdate = models.DateTimeField(auto_now_add=True)
    mother = models.ForeignKey(
        'MotherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    father = models.ForeignKey(
        'FatherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    is_ill = models.BooleanField(default=False)
    current_type = models.CharField(
        choices=(
            (DIED := 'D', 'DIED'),
            (BUNNY := 'B', 'BUNNY'),
            (FATTENING := 'F', 'FATTENING'),
            (FATHER := 'P', 'FATHER'),
            (MOTHER := 'M', 'MOTHER')
        ),
        max_length=1
    )


class DeathRabbit(BaseRabbit):
    death_date = models.DateField(auto_now_add=True)
    death_cause = models.CharField(
        choices=(
            (SLAUGHTER := 'S', 'SLAUGHTER'),
            (MOTHER := 'M', 'MOTHER'),
            (ILLNESS := 'I', 'ILLNESS'),
            (DISEASE := 'D', 'DISEASE'),
            (HEAT := 'H', 'HEAT'),
            (COOLING := 'C', 'COOLING'),
            (EXTRA := 'E', 'EXTRA')
        ),
        max_length=1
    )


class FatteningRabbit(BaseRabbit):
    is_male = models.BooleanField(null=True, blank=True)
    cage = models.ForeignKey(
        FatteningCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )


class Bunny(BaseRabbit):
    need_jigging = models.BooleanField(default=False)
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )


class MotherRabbit(BaseRabbit):
    status = MultiSelectField(
        choices=(
            (PREGNANT := 'P', 'PREGNANT'),
            (FEEDS := 'F', 'FEEDS')
        ),
        blank=True, default='', max_choices=2
    )
    last_childbirth = models.DateField(null=True, blank=True)
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )


class FatherRabbit(BaseRabbit):
    is_resting = models.BooleanField(default=True)
    cage = models.ForeignKey(
        BaseCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )
