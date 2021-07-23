from __future__ import annotations

from typing import Union, Iterable

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
        if isinstance(self, (FatteningCage, MotherCage)):
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
    
    # FIXME: to manager
    @property
    def rabbits(self) -> set['api_models.Rabbit']:
        raise NotImplementedError
    
    def get_absolute_url(self):
        raise NotImplementedError
    
    def clean_for_jigging(self):
        if self.NEED_REPAIR in self.status:
            raise ValidationError('This cage needs repair')
        if self.NEED_CLEAN in self.status:
            raise ValidationError('This cage needs cleaning')


class FatteningCage(Cage):
    CHAR_TYPE = 'F'
    
    @property
    def rabbits(self):
        rabbit_set = set(
            self.fatteningrabbit_set.filter(
                current_type=api_models.Rabbit.TYPE_FATTENING
            )
        )
        rabbit_set.update(
            self.fatherrabbit_set.filter(current_type=api_models.Rabbit.TYPE_FATHER)
        )
        return rabbit_set
    
    def get_absolute_url(self):
        return reverse('fattening_cage__detail__url', kwargs={'id': self.id})
    
    def clean(self):
        super().clean()
        rabbits = list(self.rabbits)
        if len(rabbits) > 0:
            if len(rabbits) == 1:
                rabbit = rabbits[0]
                self._clean_for_father(rabbit)
            else:
                self._clean_for_fattening(self.rabbits)
    
    def clean_for_jigging_father(self):
        self.clean_for_jigging()
        if self.fatherrabbit_set.filter(
            current_type=api_models.Rabbit.TYPE_FATHER
        ).count() > 0:
            raise ValidationError('Father rabbit is already sitting in this cage')
    
    def clean_for_jigging_rabbits(self, rabbits: Iterable['api_models.Rabbit']):
        self.clean_for_jigging()
        self._clean_for_rabbits(rabbits)
    
    @staticmethod
    def _clean_for_rabbits(rabbits: Iterable['api_models.Rabbit']):
        rabbits = list(rabbits)
        if len(rabbits) == 0:
            return
        for rabbit in rabbits[1:]:
            if rabbit.is_male != rabbits[0].is_male:
                raise ValidationError('Rabbits in the same cage must be of the same sex')
            if rabbit.is_vaccinated != rabbits[0].is_vaccinated:
                raise ValidationError(
                    'Rabbits in the same cage must be born on the same day'
                )
            if rabbit.birthday.date() != rabbits[0].birthday.date():
                raise ValidationError(
                    'Rabbits in the same cage must be of the same vaccinate status'
                )
            if rabbit.mother != rabbits[0].mother or rabbit.father != rabbits[0].father:
                raise ValidationError('Rabbits in one cage must have the same parents')
    
    def _clean_for_father(self, father: 'api_models.Rabbit'):
        if father.current_type != api_models.Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not currently FatherRabbit')
        if self.fatherrabbit_set.exclude(id=father.id).filter(
            current_type=api_models.Rabbit.TYPE_FATHER
        ).count() > 0:
            raise ValidationError('Father rabbit is already sitting in this cage')
    
    def _clean_for_fattening(self, rabbits: Iterable['api_models.Rabbit']):
        self._clean_for_rabbits(rabbits)
        for rabbit in rabbits:
            if rabbit.current_type != api_models.Rabbit.TYPE_FATTENING:
                raise ValidationError(
                    'Only fattening rabbits can sit in this cage'
                )


class MotherCage(Cage):
    CHAR_TYPE = 'M'
    
    is_parallel = models.BooleanField(default=False)
    
    @property
    def rabbits(self):
        rabbit_set = set(
            self.motherrabbit_set.filter(current_type=api_models.Rabbit.TYPE_MOTHER)
        )
        rabbit_set.update(
            self.bunny_set.filter(current_type=api_models.Rabbit.TYPE_BUNNY)
        )
        return rabbit_set
    
    def get_absolute_url(self):
        return reverse('mother_cage__detail__url', kwargs={'id': self.id})
    
    def clean(self):
        super().clean()
        rabbits = list(self.rabbits)
        if len(rabbits) > 0:
            if len(rabbits) == 1:
                self._clean_for_mother(rabbits[0])
    
    def clean_for_jigging_mother(self):
        self.clean_for_jigging()
        if (self.motherrabbit_set.filter(
            current_type=api_models.Rabbit.TYPE_MOTHER
        ).count()) > 0:
            raise ValidationError('Mother rabbit is already sitting in this cage')
    
    def _clean_for_mother(self, mother: 'api_models.Rabbit'):
        if mother.current_type != api_models.Rabbit.TYPE_MOTHER:
            raise ValidationError('This rabbit is not currently MotherRabbit')
        if self.motherrabbit_set.exclude(id=mother.id).filter(
            current_type=api_models.Rabbit.TYPE_FATHER
        ).count() > 0:
            raise ValidationError('Mother rabbit is already sitting in this cage')
