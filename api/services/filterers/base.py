from abc import ABC
from typing import Union

from django.db.models import QuerySet

__all__ = ['BaseFilterer']


class BaseFilterer(ABC):
    def __init__(self, queryset: QuerySet):
        self.queryset: QuerySet = queryset
    
    def filter(self, **kwargs) -> None:
        raise NotImplementedError
    
    def order_by(self, order) -> Union[QuerySet, list]:
        return self.queryset
