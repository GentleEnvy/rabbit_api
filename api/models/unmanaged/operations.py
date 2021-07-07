# TODO: check timezone
from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import Any, Final

from api.models import *
from api.utils.functions import to_datetime

__all__ = ['BirthOperation', 'SlaughterOperation']


class _BaseOperation(ABC):
    CHAR_TYPE: str

    time: datetime
    rabbit_id: int

    @classmethod
    def search(
            cls, rabbit_id: int = None, time_from: datetime = None,
            time_to: datetime = None
    ) -> list[_BaseOperation]:
        raise NotImplementedError

    def serialize(self) -> dict[str, Any]:
        return {
            'type': self.CHAR_TYPE,
            'time': self.time,
            'rabbit_id': self.rabbit_id
        }


class BirthOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'B'

    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        filters = {}
        if rabbit_id is not None:
            filters['id'] = rabbit_id
        if time_from is not None:
            filters['birthday__gt'] = time_from
        if time_to is not None:
            filters['birthday__lt'] = time_to
        queryset = Bunny.objects.filter(**filters)
        operations = []
        for bunny_info in queryset.values('id', 'birthday'):
            operations.append(BirthOperation(**bunny_info))
        return operations

    def __init__(self, id, birthday):
        super().__init__()
        self.time = birthday
        self.rabbit_id = id


class SlaughterOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'S'

    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        filters = {}
        if rabbit_id is not None:
            filters['id'] = rabbit_id
        if time_from is not None:
            filters['death_date__gt'] = time_from
        if time_to is not None:
            filters['death_date__lt'] = time_to
        queryset = DeadRabbit.objects.filter(
            death_cause=DeadRabbit.CAUSE_SLAUGHTER, **filters
        )
        operations = []
        for dead_rabbit_info in queryset.values('id', 'death_date'):
            operations.append(SlaughterOperation(**dead_rabbit_info))
        return operations

    def __init__(self, id, death_date):
        super().__init__()
        self.time = to_datetime(death_date)
        self.rabbit_id = id