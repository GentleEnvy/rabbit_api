from abc import ABC
from typing import Union, Type

from django.db import models
from django.db.models import QuerySet

__all__ = ['BaseFilterer']


class BaseFilterer(ABC):
    model: Type[models.Model]
    
    def __init__(self, queryset: QuerySet = None):
        if queryset is None:
            self.queryset: QuerySet = self.model.objects
        else:
            self.queryset: QuerySet = queryset
    
    def filter(self, **kwargs) -> None:
        raise NotImplementedError
    
    def order_by(self, order) -> Union[QuerySet, list]:
        return self.queryset
