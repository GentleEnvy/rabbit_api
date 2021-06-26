from __future__ import annotations

from typing import Final, Any

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from multiselectfield import MultiSelectField

from api.models._base import BaseModel
from api.models._cages import Cage, FatteningCage, MotherCage

__all__ = [
    'Rabbit', 'DeadRabbit', 'FatteningRabbit', 'Bunny', 'MotherRabbit', 'FatherRabbit'
]

_is_valid_cage = {'status': []}


class Rabbit(BaseModel):
    birthdate = models.DateField(default=now)
    mother = models.ForeignKey(
        'MotherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    father = models.ForeignKey(
        'FatherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    is_male = models.BooleanField(null=True, blank=True)
    is_ill = models.BooleanField(default=False)
    current_type = models.CharField(
        choices=(
            (TYPE_DIED := 'D', 'TYPE_DEAD'),
            (TYPE_BUNNY := 'B', 'TYPE_BUNNY'),
            (TYPE_FATTENING := 'F', 'TYPE_FATTENING'),
            (TYPE_FATHER := 'P', 'TYPE_FATHER'),
            (TYPE_MOTHER := 'M', 'TYPE_MOTHER')
        ),
        max_length=1, default=TYPE_BUNNY
    )

    CHAR_TYPE: str = None

    @classmethod
    def cast_to(cls, rabbit):
        if cls is Rabbit:
            raise NotImplementedError("rabbit can't be cast to Rabbit (base class)")
        if cls.CHAR_TYPE is None:
            raise NotImplementedError('CHAR_TYPE must be determined')
        casted_rabbit: Any = cls(rabbit_ptr=rabbit)
        casted_rabbit.__dict__.update(rabbit.__dict__)
        casted_rabbit.current_type = cls.CHAR_TYPE
        return casted_rabbit

    def get_absolute_url(self) -> str:
        if self.current_type == self.TYPE_DIED:
            return reverse('dead_rabbit_url', kwargs={'id': self.id})
        elif self.current_type == self.TYPE_BUNNY:
            return reverse('bunny_url', kwargs={'id': self.id})
        elif self.current_type == self.TYPE_FATTENING:
            return reverse('fattening_rabbit_url', kwargs={'id': self.id})
        elif self.current_type == self.TYPE_FATHER:
            return reverse('father_rabbit_url', kwargs={'id': self.id})
        elif self.current_type == self.TYPE_MOTHER:
            return reverse('mother_rabbit_url', kwargs={'id': self.id})
        raise ValidationError('Incorrect current_type')


class DeadRabbit(Rabbit):
    death_date = models.DateField(auto_now_add=True)
    death_cause = models.CharField(
        choices=(
            (CAUSE_SLAUGHTER := 'S', 'CAUSE_SLAUGHTER'),
            (CAUSE_MOTHER := 'M', 'CAUSE_MOTHER'),
            (CAUSE_ILLNESS := 'I', 'CAUSE_ILLNESS'),
            (CAUSE_DISEASE := 'D', 'CAUSE_DISEASE'),
            (CAUSE_HEAT := 'H', 'CAUSE_HEAT'),
            (CAUSE_COOLING := 'C', 'CAUSE_COOLING'),
            (CAUSE_EXTRA := 'E', 'CAUSE_EXTRA')
        ),
        max_length=1
    )

    CHAR_TYPE: Final[str] = Rabbit.TYPE_DIED

    @classmethod
    def cast_to(cls, rabbit: Rabbit) -> DeadRabbit:
        return super().cast_to(rabbit)


class FatteningRabbit(Rabbit):
    cage = models.ForeignKey(
        FatteningCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )

    def clean(self):
        if self.is_male is None:
            raise ValidationError('The sex of the FatteningRabbit must be determined')

    CHAR_TYPE: Final[str] = Rabbit.TYPE_FATTENING

    @classmethod
    def cast_to(cls, rabbit: Rabbit) -> FatteningRabbit:
        return super().cast_to(rabbit)


class Bunny(Rabbit):
    need_jigging = models.BooleanField(default=False)
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )

    CHAR_TYPE: Final[str] = Rabbit.TYPE_BUNNY

    @classmethod
    def cast_to(cls, rabbit: Rabbit) -> Bunny:
        return super().cast_to(rabbit)


class MotherRabbit(Rabbit):
    status = MultiSelectField(
        choices=(
            (STATUS_PREGNANT := 'P', 'STATUS_PREGNANT'),
            (STATUS_FEEDS := 'F', 'STATUS_FEEDS')
        ),
        blank=True, default='', max_choices=2
    )
    last_childbirth = models.DateField(null=True, blank=True)
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )

    CHAR_TYPE: Final[str] = Rabbit.TYPE_MOTHER

    @classmethod
    def cast_to(cls, rabbit: Rabbit) -> MotherRabbit:
        return super().cast_to(rabbit)

    def clean(self):
        if self.is_male is None:
            raise ValidationError('The sex of the MotherRabbit must be determined')
        if self.is_male:
            raise ValidationError('MotherRabbit must be a female')


class FatherRabbit(Rabbit):
    is_resting = models.BooleanField(default=True)
    cage = models.ForeignKey(
        Cage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )

    CHAR_TYPE: Final[str] = Rabbit.TYPE_FATHER

    @classmethod
    def cast_to(cls, rabbit: Rabbit) -> FatherRabbit:
        return super().cast_to(rabbit)

    def clean(self):
        if self.is_male is None:
            raise ValidationError('The sex of the MotherRabbit must be determined')
        if not self.is_male:
            raise ValidationError('MotherRabbit must be a male')
