from __future__ import annotations

from typing import Union

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from model_utils.managers import InheritanceManager
from multiselectfield import MultiSelectField

from api.models.base import BaseModel
from api.services.model.cage.cleaners.mixins import *
from api.services.model.cage.managers.mixins import *

__all__ = ['Cage', 'FatteningCage', 'MotherCage']


class Cage(CageCleanerMixin, CageManagerMixin, BaseModel):
    class Meta(BaseModel.Meta):
        unique_together = ('farm_number', 'number', 'letter')

    CHAR_TYPE: str = None
    objects = InheritanceManager()
    
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
        if isinstance(self, (FatteningCage, MotherCage)):
            return self
        if (casted_cage := getattr(self, 'fatteningcage', None)) is None:
            casted_cage = getattr(self, 'mothercage', None)
        if casted_cage is None:
            raise TypeError('The cage type is not defined')
        return casted_cage
    
    def __str__(self):
        return f'{self.farm_number}->{self.number}-{self.letter}'


class FatteningCage(FatteningCageCleanerMixin, FatteningCageManagerMixin, Cage):
    CHAR_TYPE = 'F'


class MotherCage(MotherCageCleanerMixin, MotherCageManagerMixin, Cage):
    CHAR_TYPE = 'M'
    
    has_right_womb = models.BooleanField(default=False)
    womb = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
