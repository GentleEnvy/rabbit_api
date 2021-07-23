from abc import ABC
from typing import Union, Type

from django.db import models
from django.db.models import QuerySet

__all__ = ['BaseFilterer']


class BaseFilterer(ABC):
    model: Type[models.Model]
    
    def __init__(self, queryset: QuerySet = None):
        self.queryset: QuerySet = queryset or self.model.objects.all()
    
    def filter(self, **kwargs) -> None:
        raise NotImplementedError
    
    def order_by(self, order) -> Union[QuerySet, list]:
        return self.queryset
