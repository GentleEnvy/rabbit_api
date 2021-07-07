from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Final

from api.models import Bunny

__all__ = ['BirthOperation']


class _BaseOperation(ABC):
    CHAR_TYPE: str

    @classmethod
    def search(
            cls, rabbit_id: int = None, time_from: datetime = datetime.min,
            time_to: datetime = datetime.max
    ) -> list[_BaseOperation]:
        raise NotImplementedError

    @property
    @abstractmethod
    def time(self) -> datetime:
        raise NotImplementedError

    @property
    @abstractmethod
    def rabbit_id(self) -> int:
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
    def search(cls, rabbit_id=None, time_from=datetime.min, time_to=datetime.max):
        filters = {}
        if rabbit_id is not None:
            filters['id'] = rabbit_id
        queryset = Bunny.objects.filter(
            birthday__gt=time_from, birthday__lt=time_to, **filters
        )
        operations = []
        for bunny_info in queryset.all():
            operations.append(BirthOperation(**bunny_info))
        return operations

    def __init__(self, id, birthday):
        self._time = birthday
        self._rabbit_id = id

    @property
    def time(self):
        return self._time

    @property
    def rabbit_id(self):
        return self._rabbit_id
