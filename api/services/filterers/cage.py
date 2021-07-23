from api.models import *
from api.services.filterers.base import BaseFilterer

__all__ = ['CageFilterer']


class CageFilterer(BaseFilterer):
    model = Cage
    
    def filter(self):
        pass
    
    def order_by_nearest_to(self, cage: Cage) -> list[Cage]:
        cages = list(self.queryset.order_by('farm_number', 'number', 'letter'))
        index = cages.index(cage)
        ordered_cages = []
        increment_index = index
        decrement_index = index
        while decrement_index >= 0 or increment_index <= len(cages):
            increment_index += 1
            decrement_index -= 1
            try:
                ordered_cages.append(cages[increment_index])
            except IndexError:
                pass
            try:
                ordered_cages.append(cages[decrement_index])
            except IndexError:
                pass
        return ordered_cages
