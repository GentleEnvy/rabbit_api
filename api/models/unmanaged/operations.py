from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import Any, Final, Optional

from api.models import *
from api.utils.functions import to_datetime

__all__ = [
    'BirthOperation', 'SlaughterOperation', 'VaccinationOperation', 'MatingOperation',
    'JiggingOperation'
]


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


class VaccinationOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'V'

    # noinspection SpellCheckingInspection
    _relation_id_fields = (
        'bunnyhistory__rabbit_id', 'fatteningrabbithistory__rabbit_id',
        'motherrabbithistory__rabbit_id', 'fatherrabbithistory__rabbit_id'
    )

    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        filters = {}
        if rabbit_id is not None:
            for relation_id_field in cls._relation_id_fields:
                filters[relation_id_field] = rabbit_id
        if time_from is not None:
            filters['time__gt'] = time_from
        if time_to is not None:
            filters['time__lt'] = time_to
        queryset = RabbitHistory.objects.filter(is_vaccinated=True, **filters)
        operations = []
        for rabbit_history_info in queryset.values('time', *cls._relation_id_fields):
            try:
                operations.append(VaccinationOperation(**rabbit_history_info))
            except ValueError:
                continue
        return operations

    def __init__(self, time, **relation_id_fields):
        super().__init__()
        self.time = time
        try:
            self.rabbit_id = [
                value for key, value in relation_id_fields.items()
                if value is not None and key in self._relation_id_fields
            ][0]
        except IndexError:
            raise ValueError


class MatingOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'M'

    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        filters = {}
        if rabbit_id is not None:
            if Rabbit.objects.get(id=rabbit_id).is_male:
                filters['father_rabbit_id'] = rabbit_id
            else:
                filters['mother_rabbit_id'] = rabbit_id
        if time_from is not None:
            filters['time__gt'] = time_from
        if time_to is not None:
            filters['time__lt'] = time_to
        queryset = Mating.objects.filter(
            **filters
        )
        operations = []
        for mating_info in queryset.values(
                'time', 'father_rabbit_id', 'mother_rabbit_id'
        ):
            operations.append(MatingOperation(**mating_info))
        return operations

    def __init__(self, time, father_rabbit_id, mother_rabbit_id):
        super().__init__()
        self.time = time
        self.rabbit_id = father_rabbit_id
        self.mother_rabbit_id = mother_rabbit_id

    def serialize(self):
        super_serialize = super().serialize()
        super_serialize['father_rabbit_id'] = super_serialize.pop('rabbit_id')
        return super_serialize | {'mother_rabbit_id': self.mother_rabbit_id}


class JiggingOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'J'

    # noinspection SpellCheckingInspection
    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        rabbits = Rabbit.objects.filter(
            **({} if rabbit_id is None else {'id': rabbit_id})
        ).select_related(
            'bunny', 'fatteningrabbit', 'motherrabbit', 'fatherrabbit'
        ).prefetch_related(
            'bunny__bunnyhistory_set', 'bunny__bunnyhistory_set__cage',
            *['fatteningrabbit__fatteningrabbithistory_set',
              'fatteningrabbit__fatteningrabbithistory_set__cage'],
            *['motherrabbit__motherrabbithistory_set',
              'motherrabbit__motherrabbithistory_set__cage'],
            *['fatherrabbit__fatherrabbithistory_set',
              'fatherrabbit__fatherrabbithistory_set__cage']
        )
        operations = []
        for rabbit in rabbits:
            histories = []
            for attr in ('bunny', 'fatteningrabbit', 'motherrabbit', 'fatherrabbit'):
                if hasattr(rabbit, attr):
                    for history in getattr(
                            getattr(rabbit, attr), attr + 'history_set'
                    ).all():
                        if history.cage is not None:
                            histories.append({
                                'time': history.time,
                                'cage': history.cage
                            })
            if len(histories) > 1:
                histories.sort(key=lambda h: h['time'])
                prev = histories[0]
                for history in histories[1:]:
                    if cls._check_time(history['time'], time_from, time_to):
                        operations.append(JiggingOperation(
                            rabbit_id=rabbit.id,
                            time=history['time'],
                            old_cage={
                                'farm_number': prev['cage'].farm_number,
                                'number': prev['cage'].number,
                                'letter': prev['cage'].letter
                            },
                            new_cage={
                                'farm_number': history['cage'].farm_number,
                                'number': history['cage'].number,
                                'letter': history['cage'].letter
                            }
                        ))
        return operations

    def __init__(self, rabbit_id, time, old_cage: dict, new_cage: dict):
        super().__init__()
        self.rabbit_id = rabbit_id
        self.time = time
        self.old_cage = old_cage
        self.new_cage = new_cage

    def serialize(self):
        return super().serialize() | {
            'old_cage': self.old_cage,
            'new_cage': self.new_cage
        }

    @staticmethod
    def _check_time(
            time: datetime, from_: Optional[datetime], to: Optional[datetime]
    ) -> bool:
        if from_ is not None and time < from_ or to is not None and time > to:
            return False
        return True
