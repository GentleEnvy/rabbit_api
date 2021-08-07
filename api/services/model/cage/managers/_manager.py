from typing import Final

from django.db.models import Prefetch, Count, Q, QuerySet
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
                queryset=models.MotherRabbit.all_current.all(), to_attr='mother_rabbits'
            ),
            Prefetch(
                'mothercage__bunny_set', queryset=models.Bunny.all_current.all(),
                to_attr='bunnies'
            ),
            Prefetch(
                'fatteningcage__fatherrabbit_set',
                queryset=models.FatherRabbit.all_current.all(), to_attr='father_rabbits'
            ),
            Prefetch(
                'fatteningcage__fatteningrabbit_set',
                queryset=models.FatteningRabbit.all_current.all(),
                to_attr='fattening_rabbits'
            )
        )
    
    @classmethod
    def prefetch_number_rabbits(cls) -> InheritanceQuerySet:
        Rabbit = models.Rabbit
        return models.Cage.objects.select_subclasses().annotate(
            number_rabbits=Count(
                'mothercage__motherrabbit',
                filter=Q(mothercage__motherrabbit__current_type=Rabbit.TYPE_MOTHER)
            ) + Count(
                'mothercage__bunny',
                filter=Q(mothercage__bunny__current_type=Rabbit.TYPE_BUNNY)
            ) + Count(
                'fatteningcage__fatteningrabbit',
                filter=Q(
                    fatteningcage__fatteningrabbit__current_type=Rabbit.TYPE_FATTENING
                )
            ) + Count(
                'fatteningcage__fatherrabbit',
                filter=Q(
                    fatteningcage__fatherrabbit__current_type=Rabbit.TYPE_FATHER
                )
            )
        )
    
    @property
    def rabbits(self) -> list:
        rabbits = []
        manager = self.cage.cast.manager
        rabbits.extend(getattr(manager, 'mother_rabbits', []))
        rabbits.extend(getattr(manager, 'bunnies', []))
        rabbits.extend(getattr(manager, 'fattening_rabbits', []))
        rabbits.extend(getattr(manager, 'father_rabbits', []))
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
                queryset=models.MotherRabbit.all_current.all(), to_attr='mother_rabbits'
            ),
            Prefetch(
                'bunny_set', queryset=models.Bunny.all_current.all(), to_attr='bunnies'
            )
        )
    
    @property
    def mother_rabbits(self):
        if (mother_rabbits := getattr(self.cage, 'mother_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (
                mother_rabbits := getattr(self.cage.mothercage, 'mother_rabbits', None)
            ) is None:
                return self.cage.motherrabbit_set.filter(
                    current_type=models.Rabbit.TYPE_MOTHER
                )
        return mother_rabbits
    
    @property
    def bunnies(self):
        if (bunnies := getattr(self.cage, 'bunnies', None)) is None:
            # noinspection PyUnresolvedReferences
            if (bunnies := getattr(self.cage.mothercage, 'bunnies', None)) is None:
                return self.cage.bunny_set.filter(current_type=models.Rabbit.TYPE_BUNNY)
        return bunnies
    
    @property
    def is_parallel(self) -> bool:
        return not self.cage.has_right_womb


class FatteningCageManager(CageManager):
    cage: 'models.FatteningCage'
    
    @classmethod
    def prefetch_rabbits(cls) -> QuerySet:
        return models.MotherCage.objects.prefetch_related(
            Prefetch(
                'fatherrabbit_set',
                queryset=models.FatherRabbit.all_current.all(), to_attr='father_rabbits'
            ),
            Prefetch(
                'fatteningrabbit_set',
                queryset=models.FatteningRabbit.all_current.all(),
                to_attr='fattening_rabbits'
            )
        )
    
    @property
    def father_rabbits(self):
        if (father_rabbits := getattr(self.cage, 'father_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (
                father_rabbits := getattr(self.cage.fatteningcage, 'father_rabbits', None)
            ) is None:
                return self.cage.fatherrabbit_set.filter(
                    current_type=models.Rabbit.TYPE_FATHER
                )
        return father_rabbits
    
    @property
    def fattening_rabbits(self):
        if (fattening_rabbits := getattr(self.cage, 'fattening_rabbits', None)) is None:
            # noinspection PyUnresolvedReferences
            if (fattening_rabbits := getattr(
                self.cage.fatteningcage, 'fattening_rabbits', None
            )) is None:
                return self.cage.fatherrabbit_set.filter(
                    current_type=models.Rabbit.TYPE_FATTENING
                )
        return fattening_rabbits
