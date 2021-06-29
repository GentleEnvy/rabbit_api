from __future__ import annotations

from typing import Union

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from multiselectfield import MultiSelectField

from api.models.base import BaseModel

__all__ = ['Cage', 'FatteningCage', 'MotherCage']


class Cage(BaseModel):
    class Meta:
        unique_together = ('farm_number', 'number', 'letter')

    farm_number = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(4)]
    )
    number = models.IntegerField()
    letter = models.CharField(
        choices=(
            (LETTER_A := 'а', 'LETTER_A'),
            (LETTER_B := 'б', 'LETTER_B'),
            (LETTER_V := 'в', 'LETTER_V'),
            (LETTER_G := 'г', 'LETTER_G')
        ),
        max_length=1, default=LETTER_A
    )
    status = MultiSelectField(
        choices=(STATUS_CHOICES := (
            (NEED_CLEAN := 'C', 'NEED_CLEAN'),
            (NEED_REPAIR := 'R', 'NEED_REPAIR')
        )),
        blank=True, default='', max_choices=2
    )

    # noinspection PyUnresolvedReferences
    @property
    def cast(self) -> Union[FatteningCage, MotherCage]:
        if isinstance(self, FatteningCage) or isinstance(self, MotherCage):
            return self
        try:
            return self.fatteningcage
        except Cage.fatteningcage.RelatedObjectDoesNotExist:
            pass
        try:
            return self.mothercage
        except Cage.mothercage.RelatedObjectDoesNotExist:
            pass
        raise TypeError('The cell type is not defined')

    @property
    def rabbits(self) -> set['import api.models.Rabbit']:
        raise NotImplementedError

    def get_absolute_url(self):
        raise NotImplementedError


class FatteningCage(Cage):
    @property
    def rabbits(self):
        rabbit_set = set(self.fatteningrabbit_set.all())
        rabbit_set.update(self.fatherrabbit_set.all())
        return rabbit_set

    def get_absolute_url(self):
        return reverse('fattening_cage__detail__url', kwargs={'id': self.id})


class MotherCage(Cage):
    is_parallel = models.BooleanField(default=False)

    @property
    def rabbits(self):
        rabbit_set = set(self.motherrabbit_set.all())
        rabbit_set.update(self.fatherrabbit_set.all())
        rabbit_set.update(self.bunny_set.all())
        return rabbit_set

    def get_absolute_url(self):
        return reverse('mother_cage__detail__url', kwargs={'id': self.id})
