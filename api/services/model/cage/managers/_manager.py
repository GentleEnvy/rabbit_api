from typing import Final

from django.db.models import *
from django.db.models.functions import *
from model_utils.managers import InheritanceQuerySet

import api.models as models

__all__ = [
    'CageManager', 'MotherCageManager', 'FatteningCageManager'
]


class CageManager:
    cage: 'models.Cage'
    
    def __init__(self, cage):
        self.cage: Final['models.Cage'] = cage
    
    @classmethod
    def prefetch_rabbits(cls) -> InheritanceQuerySet:
        return models.Cage.objects.select_subclasses().prefetch_related(
            Prefetch(
                'mothercage__motherrabbit_set',
                queryset=models.MotherRabbit.objects.all(), to_attr='mother_rabbits'
            ),
            Prefetch(
                'mothercage__bunny_set', queryset=models.Bunny.objects.all(),
                to_attr='bunnies'
            ),
            Prefetch(
                'fatteningcage__fatherrabbit_set',
                queryset=models.FatherRabbit.objects.all(), to_attr='father_rabbits'
            ),
            Prefetch(
                'fatteningcage__fatteningrabbit_set',
                queryset=models.FatteningRabbit.objects.all(),
                to_attr='fattening_rabbits'
            )
        )
    
    @classmethod
    def prefetch_number_rabbits(cls) -> InheritanceQuerySet:
        return models.Cage.objects.select_subclasses().annotate(
            number_rabbits=Count('mothercage__motherrabbit') + Count(
                'mothercage__bunny'
            ) + Count('fatteningcage__fatteningrabbit') + Count(
                'fatteningcage__fatherrabbit'
            )
        )
    
    @property
    def rabbits(self) -> list:
        rabbits = []
        manager_ = self.cage.cast.manager
        rabbits.extend(getattr(manager_, 'mother_rabbits', []))
        rabbits.extend(getattr(manager_, 'bunnies', []))
        rabbits.extend(getattr(manager_, 'fattening_rabbits', []))
        rabbits.extend(getattr(manager_, 'father_rabbits', []))
        return rabbits
    
    @property
    def number_rabbits(self) -> int:
        if (number_rabbits := getattr(self.cage, 'number_rabbits', None)) is None:
            return len(self.rabbits)
        return number_rabbits


class MotherCageManager(CageManager):
    cage: 'models.MotherCage'
    
    BUNNIES_NAME = 'bunnies'
    
    @classmethod
    def prefetch_rabbits(cls) -> QuerySet:
        return models.MotherCage.objects.prefetch_related(
            Prefetch(
                'motherrabbit_set',
                queryset=models.MotherRabbit.objects.all(), to_attr='mother_rabbits'
            ),
            Prefetch(
                'bunny_set', queryset=models.Bunny.objects.all(), to_attr='bunnies'
            )
        )
    
    @classmethod
    def prefetch_number_rabbits(cls, queryset=None) -> QuerySet:
        if queryset is None:
            queryset = super().prefetch_number_rabbits()
        return queryset.filter(~Q(mothercage=None))
    
    @classmethod
    def prefetch_womb_cage_id(cls, queryset=None) -> QuerySet:
        if queryset is None:
            queryset = models.MotherCage.objects.all()
        return queryset.select_related('womb', 'ref_womb')
    
    @property
    def mother_rabbits(self):
        if (mother_rabbits := getattr(self.cage, 'mother_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (
                mother_rabbits := getattr(self.cage.mothercage, 'mother_rabbits', None)
            ) is None:
                return self.cage.motherrabbit_set.all()
        return mother_rabbits
    
    @property
    def bunnies(self):
        if (bunnies := getattr(self.cage, 'bunnies', None)) is None:
            # noinspection PyUnresolvedReferences
            if (bunnies := getattr(self.cage.mothercage, 'bunnies', None)) is None:
                return self.cage.bunny_set.all()
        return bunnies
    
    @property
    def womb_cage(self) -> 'models.MotherCage | None':
        if (womb := self.cage.womb) is None:
            return self.cage.ref_womb
        return womb
    
    @property
    def is_parallel(self) -> bool:
        return self.womb_cage is None


class FatteningCageManager(CageManager):
    cage: 'models.FatteningCage'
    
    @classmethod
    def prefetch_rabbits(cls) -> QuerySet:
        return models.FatteningCage.objects.prefetch_related(
            Prefetch(
                'fatherrabbit_set',
                queryset=models.FatherRabbit.objects.all(), to_attr='father_rabbits'
            ),
            Prefetch(
                'fatteningrabbit_set',
                queryset=models.FatteningRabbit.objects.all(),
                to_attr='fattening_rabbits'
            )
        )
    
    @classmethod
    def prefetch_number_rabbits(cls) -> QuerySet:
        return super().prefetch_number_rabbits().filter(~Q(fatteningcage=None))
    
    @property
    def father_rabbits(self):
        if (father_rabbits := getattr(self.cage, 'father_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (
                father_rabbits := getattr(self.cage.fatteningcage, 'father_rabbits', None)
            ) is None:
                return self.cage.fatherrabbit_set.all()
        return father_rabbits
    
    @property
    def fattening_rabbits(self):
        if (fattening_rabbits := getattr(self.cage, 'fattening_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (fattening_rabbits := getattr(
                self.cage.fatteningcage, 'fattening_rabbits', None
            )) is None:
                return self.cage.fatteningrabbit_set.all()
        return fattening_rabbits
