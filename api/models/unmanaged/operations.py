from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from api.models import Bunny


class _BaseOperation(ABC):
    CHAR_TYPE: str
    ORDER_BY_TIME = 'T'

    @classmethod
    def search(
            cls, rabbit_id: int = None, time_from: datetime = datetime.min,
            time_to: datetime = datetime.max, order_by=ORDER_BY_TIME
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
    CHAR_TYPE = 'B'
    ORDER_BY_TIME = '-birthday'

    @classmethod
    def search(
            cls, rabbit_id=None, time_from=datetime.min, time_to=datetime.max,
            order_by=ORDER_BY_TIME
    ):
        filters = {}
        if rabbit_id is not None:
            filters['id'] = rabbit_id
        queryset = Bunny.objects.filter(
            birthday__gt=time_from, birthday__lt=time_to, **filters
        ).order_by(order_by)
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
