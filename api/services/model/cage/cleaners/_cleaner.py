from typing import Final, Iterable

from django.core.exceptions import ValidationError
from django.db.models import Q

import api.models as models

__all__ = ['CageCleaner', 'FatteningCageCleaner', 'MotherCageCleaner']


class CageCleaner:
    cage: 'models.Cage'
    
    def __init__(self, cage):
        self.cage: Final['models.Cage'] = cage
    
    def clean(self):
        pass
    
    def for_jigging(self):
        if models.Cage.NEED_REPAIR in self.cage.status:
            raise ValidationError('This cage needs repair')
        if models.Cage.NEED_CLEAN in self.cage.status:
            raise ValidationError('This cage needs cleaning')
    
    def for_task(self):
        id = self.cage.id
        if models.Task.objects.filter(
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


class FatteningCageCleaner(CageCleaner):
    cage: 'models.FatteningCage'
    
    def clean(self):
        super().clean()
        rabbits = list(self.cage.manager.rabbits)
        if len(rabbits) > 0:
            if rabbits[0].current_type == models.Rabbit.TYPE_FATHER:
                self._for_father(rabbits[0])
            else:
                self._for_fattening(rabbits)
    
    def clean_for_jigging_father(self):
        self.for_jigging()
        if len(self.cage.manager.father_rabbits) > 0:
            raise ValidationError('Father rabbit is already sitting in this cage')
    
    def clean_for_jigging_bunnies(self, rabbits: Iterable['models.Rabbit']):
        rabbits = list(rabbits)
        if len(rabbits) == 0:
            return
        self.for_jigging()
        if len(self.cage.manager.rabbits) > 0:
            raise ValidationError('The cage for jigging bunnies should be empty')
        self._for_rabbits(rabbits)
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
    def _for_rabbits(rabbits: list['models.Rabbit']):
        for rabbit in rabbits[1:]:
            if rabbit.is_male != rabbits[0].is_male:
                raise ValidationError('Rabbits in the same cage must be of the same sex')
            if rabbit.is_vaccinated != rabbits[0].is_vaccinated:
                raise ValidationError(
                    'Rabbits in the same cage must be born on the same day'
                )
    
    def _for_father(self, father: 'models.Rabbit'):
        if father.current_type != models.Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not currently FatherRabbit')
        if len(self.cage.manager.father_rabbits) > 0:
            raise ValidationError('Other father rabbit is already sitting in this cage')
        if len(self.cage.manager.fattening_rabbits) > 0:
            raise ValidationError(
                'Other fattening rabbit is already sitting in this cage'
            )
    
    def _for_fattening(self, rabbits: Iterable['models.Rabbit']):
        for rabbit in rabbits:
            if rabbit.current_type != models.Rabbit.TYPE_FATTENING:
                raise ValidationError('Only fattening rabbits can sit in this cage')
        self._for_rabbits(list(rabbits))


class MotherCageCleaner(CageCleaner):
    cage: 'models.MotherCage'
    
    def clean(self):
        super().clean()
        rabbits = list(self.cage.manager.rabbits)
        if len(rabbits) > 0:
            if len(rabbits) == 1:
                self._for_mother(rabbits[0])
        if self.cage.has_right_womb:
            try:
                models.MotherCage.objects.get(
                    farm_number=self.cage.farm_number, number=self.cage.number,
                    letter=chr(ord(self.cage.letter) + 1)
                )
            except models.MotherCage.DoesNotExist:
                raise ValidationError('There are no cages to the right of this cage')
    
    def for_jigging_mother(self):
        self.for_jigging()
        if len(self.cage.manager.mother_rabbits) > 0:
            raise ValidationError('Mother rabbit is already sitting in this cage')

    def _for_mother(self, mother: 'models.Rabbit'):
        if mother.current_type != models.Rabbit.TYPE_MOTHER:
            raise ValidationError('This rabbit is not currently MotherRabbit')
        if len(self.cage.manager.mother_rabbits) > 0:
            raise ValidationError('Mother rabbit is already sitting in this cage')
