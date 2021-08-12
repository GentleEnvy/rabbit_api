from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import Any, Final, Union

from django.db.models import F

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
            filters['birthday__gte'] = time_from
        if time_to is not None:
            filters['birthday__lte'] = time_to
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
            filters['death_day__gte'] = time_from
        if time_to is not None:
            filters['death_day__lte'] = time_to
        queryset = DeadRabbit.objects.filter(
            death_cause=DeadRabbit.CAUSE_SLAUGHTER, **filters
        )
        operations = []
        for dead_rabbit_info in queryset.values('id', 'death_day'):
            operations.append(SlaughterOperation(**dead_rabbit_info))
        return operations
    
    def __init__(self, id, death_day):
        super().__init__()
        self.time = to_datetime(death_day)
        self.rabbit_id = id


class VaccinationOperation(_BaseOperation):
    CHAR_TYPE: Final[str] = 'V'
    
    @classmethod
    def search(cls, rabbit_id=None, time_from=None, time_to=None):
        filters = {}
        if rabbit_id is not None:
            filters['id'] = rabbit_id
        if time_from is not None:
            filters['history_date__gte'] = time_from
        if time_to is not None:
            filters['history_date__lte'] = time_to
        
        histories = FatteningRabbit.history.filter(
            **filters, is_vaccinated=True
        ).annotate(rabbit=F('id')).order_by('id').distinct('id').values(
            'history_date', 'id'
        )
        return [VaccinationOperation(**history) for history in histories]
    
    def __init__(self, history_date, id):
        super().__init__()
        self.time = history_date
        self.rabbit_id = id


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
            filters['time__gte'] = time_from
        if time_to is not None:
            filters['time__lte'] = time_to
        queryset = Mating.objects.filter(**filters)
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
        histories = cls._get_histories(rabbit_id, time_to)
        return cls._extract(histories, time_from)
    
    @staticmethod
    def _get_histories(rabbit_id, time_to) -> list[dict[str, Union[int, datetime, Cage]]]:
        # TODO: order by history_date, check time_from and add first_history.prev_record
        histories = []
        for rabbit_model in Rabbit.get_subclasses():
            history = getattr(rabbit_model, 'history', None)
            if history is not None:
                histories.extend(
                    history.filter(
                        **(
                            ({} if rabbit_id is None else {'id': rabbit_id}) |
                            ({} if time_to is None else {'history_date__lte': time_to})
                        )
                    ).values('history_date', 'id', 'cage')
                )
                histories.sort(key=lambda h: h['history_date'])
        cage_id__instance = {
            c.id: c for c in Cage.objects.filter(id__in=[h['cage'] for h in histories])
        }
        for history in histories:
            history['cage'] = cage_id__instance[history['cage']]
        return histories
    
    @staticmethod
    def _extract(histories, time_from) -> list[JiggingOperation]:
        operations = []
        if len(histories) > 1:
            prev = histories[0]
            for curr in histories[1:]:
                if time_from is None or curr['history_date'] > time_from:
                    if prev['cage'].id != curr['cage'].id and prev['id'] == curr['id']:
                        operations.append(
                            JiggingOperation(
                                rabbit_id=curr['id'],
                                time=curr['history_date'],
                                old_cage={
                                    'farm_number': prev['cage'].farm_number,
                                    'number': prev['cage'].number,
                                    'letter': prev['cage'].letter
                                },
                                new_cage={
                                    'farm_number': curr['cage'].farm_number,
                                    'number': curr['cage'].number,
                                    'letter': curr['cage'].letter
                                }
                            )
                        )
                prev = curr
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
