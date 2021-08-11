from typing import Type

from model_utils.managers import InheritanceQuerySet

from api.models import *
from api.services.model.base.filterer import BaseFilterer

__all__ = ['CageFilterer']


class CageFilterer(BaseFilterer):
    queryset: InheritanceQuerySet
    model = Cage
    
    def filter(self):
        pass
    
    def order_by_nearest_to(self, cage: Cage, cage_type: Type[Cage] = Cage) -> list[Cage]:
        cages = list(self.queryset.order_by('farm_number', 'number', 'letter'))
        index = cages.index(cage)
        ordered_cages = []
        increment_index = index
        decrement_index = index
        while decrement_index >= 0 or increment_index <= len(cages):
            increment_index += 1
            decrement_index -= 1
            try:
                increment_cage = cages[increment_index]
            except IndexError:
                increment_cage = None
            try:
                decrement_cage = cages[decrement_index]
            except IndexError:
                decrement_cage = None
            for ordered_cage in (increment_cage, decrement_cage):
                if ordered_cage is not None:
                    if isinstance(ordered_cage, cage_type):
                        ordered_cages.append(ordered_cage)
        return ordered_cages
