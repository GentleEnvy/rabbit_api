from __future__ import annotations

from typing import Union

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from multiselectfield import MultiSelectField

import api.models as api_models
from api.models.base import BaseModel

__all__ = ['Cage', 'FatteningCage', 'MotherCage']


class Cage(BaseModel):
    class Meta(BaseModel.Meta):
        unique_together = ('farm_number', 'number', 'letter')
    
    CHAR_TYPE: str = None
    
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
    
    # FIXME: not counting the dead rabbits
    @property
    def rabbits(self) -> set['api_models.Rabbit']:
        raise NotImplementedError
    
    def get_absolute_url(self):
        raise NotImplementedError


class FatteningCage(Cage):
    CHAR_TYPE = 'F'
    
    @property
    def rabbits(self):
        rabbit_set = set(self.fatteningrabbit_set.all())
        rabbit_set.update(self.fatherrabbit_set.all())
        return rabbit_set
    
    def get_absolute_url(self):
        return reverse('fattening_cage__detail__url', kwargs={'id': self.id})


class MotherCage(Cage):
    CHAR_TYPE = 'M'
    
    has_right_womb = models.BooleanField(default=False)
    
    @property
    def rabbits(self):
        rabbit_set = set(self.motherrabbit_set.all())
        rabbit_set.update(self.bunny_set.all())
        return rabbit_set
    
    def clean(self):
        super().clean()
        if self.has_right_womb:
            try:
                MotherCage.objects.get(
                    farm_number=self.farm_number, number=self.number,
                    letter=chr(ord(self.letter) + 1)
                )
            except MotherCage.DoesNotExist:
                raise ValidationError('There are no cages to the right of this cage')
    
    def get_absolute_url(self):
        return reverse('mother_cage__detail__url', kwargs={'id': self.id})
