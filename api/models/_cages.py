from __future__ import annotations

from typing import Union, Iterable

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from model_utils.managers import InheritanceManager
from multiselectfield import MultiSelectField

import api.models as api_models
from api.models.base import BaseModel
from api.services.model.cage.managers.mixins import *

__all__ = ['Cage', 'FatteningCage', 'MotherCage']


class Cage(CageManagerMixin, BaseModel):
    class Meta(BaseModel.Meta):
        unique_together = ('farm_number', 'number', 'letter')
    
    objects = InheritanceManager()
    
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
    
    def __str__(self):
        return f'{self.farm_number}->{self.number}-{self.letter}'
    
    def clean_for_jigging(self):
        if self.NEED_REPAIR in self.status:
            raise ValidationError('This cage needs repair')
        if self.NEED_CLEAN in self.status:
            raise ValidationError('This cage needs cleaning')
    
    def clean_for_task(self):
        id = self.id
        if api_models.Task.objects.filter(
            Q(is_confirmed=None) & (
                Q(toreproductiontask__cage_to__id=id) |
                Q(tofatteningtask__cage_to__id=id) |
                Q(bunnyjiggingtask__male_cage_to__id=id) |
                Q(bunnyjiggingtask__female_cage_to__id=id) |
                Q(vaccinationtask__cage__id=id) |
                Q(slaughterinspectiontask__cage__id=id)
            )
        ).count() > 0:
            raise ValidationError('This cage already belongs to other Task')


class FatteningCage(FatteningCageManagerMixin, Cage):
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
    
    def clean(self):
        super().clean()
        rabbits = list(self.rabbits)
        if len(rabbits) > 0:
            if rabbits[0].current_type == api_models.Rabbit.TYPE_FATHER:
                self._clean_for_father(rabbits[0])
            else:
                self._clean_for_fattening(self.rabbits)
    
    def clean_for_jigging_father(self):
        self.clean_for_jigging()
        if self.fatherrabbit_set.filter(
            current_type=api_models.Rabbit.TYPE_FATHER
        ).count() > 0:
            raise ValidationError('Father rabbit is already sitting in this cage')
    
    def clean_for_jigging_bunnies(self, rabbits: Iterable['api_models.Rabbit']):
        rabbits = list(rabbits)
        if len(rabbits) == 0:
            return
        self.clean_for_jigging()
        if len(self.rabbits) > 0:
            raise ValidationError('The cage for jigging bunnies should be empty')
        self._clean_for_rabbits(rabbits)
        for bunny in rabbits[1:]:
            if bunny.birthday.date() != rabbits[0].birthday.date():
                raise ValidationError(
                    'Bunnies in the same cage must be born on the same day'
                )
            if bunny.mother != rabbits[0].mother or bunny.father != rabbits[0].father:
                raise ValidationError(
                    'Bunnies in the came cage must have the same parents'
                )
    
    @staticmethod
    def _clean_for_rabbits(rabbits: list['api_models.Rabbit']):
        for rabbit in rabbits[1:]:
            if rabbit.is_male != rabbits[0].is_male:
                raise ValidationError('Rabbits in the same cage must be of the same sex')
            if rabbit.is_vaccinated != rabbits[0].is_vaccinated:
                raise ValidationError(
                    'Rabbits in the same cage must be born on the same day'
                )
    
    def _clean_for_father(self, father: 'api_models.Rabbit'):
        if father.current_type != api_models.Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not currently FatherRabbit')
        if self.fatherrabbit_set.exclude(id=father.id).filter(
            current_type=api_models.Rabbit.TYPE_FATHER
        ).count() > 0:
            raise ValidationError('Other father rabbit is already sitting in this cage')
        if self.fatteningrabbit_set.exclude(id=father.id).filter(
            current_type=api_models.Rabbit.TYPE_FATTENING
        ).count() > 0:
            raise ValidationError(
                'Other fattening rabbit is already sitting in this cage'
            )
    
    def _clean_for_fattening(self, rabbits: Iterable['api_models.Rabbit']):
        for rabbit in rabbits:
            if rabbit.current_type != api_models.Rabbit.TYPE_FATTENING:
                raise ValidationError(
                    'Only fattening rabbits can sit in this cage'
                )
        self._clean_for_rabbits(list(rabbits))


class MotherCage(MotherCageManagerMixin, Cage):
    CHAR_TYPE = 'M'
    
    has_right_womb = models.BooleanField(default=False)
    
    @property
    def rabbits(self):
        rabbit_set = set(
            self.motherrabbit_set.filter(current_type=api_models.Rabbit.TYPE_MOTHER)
        )
        rabbit_set.update(
            self.bunny_set.filter(current_type=api_models.Rabbit.TYPE_BUNNY)
        )
        return rabbit_set
    
    def clean(self):
        super().clean()
        rabbits = list(self.rabbits)
        if len(rabbits) > 0:
            if len(rabbits) == 1:
                self._clean_for_mother(rabbits[0])
        if self.has_right_womb:
            try:
                MotherCage.objects.get(
                    farm_number=self.farm_number, number=self.number,
                    letter=chr(ord(self.letter) + 1)
                )
            except MotherCage.DoesNotExist:
                raise ValidationError('There are no cages to the right of this cage')
    
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
