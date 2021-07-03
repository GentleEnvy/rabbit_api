from abc import ABC
from datetime import date, timedelta, datetime
from typing import Final, Optional, Union
import random

from api.managers import *
from api.services.forecast.rabbit._condition import ForecastCondition
from api.utils.functions import diff_time

__all__ = [
    'BaseRabbitFuture', 'BunnyFuture', 'FatteningRabbitFuture', 'MotherRabbitFuture',
    'FatherRabbitFuture'
]


class BaseRabbitFuture(ABC):
    def __init__(self, birthdate: date, status: set[str], id: int = None, **_):
        self.id: Final[Optional[int]] = id
        self.birthdate: Final[date] = birthdate
        self.status: Final[set[str]] = status

    def age(self, target_date: Union[date, datetime]) -> timedelta:
        return diff_time(target_date, self.birthdate)

    def tomorrow_state(self, condition: ForecastCondition) -> None:
        raise NotImplementedError


class BunnyFuture(BaseRabbitFuture):
    DEFAULT_DEATH_PROBABILITY: Final[float] = 0.07

    def tomorrow_state(
            self, condition, death_probability=DEFAULT_DEATH_PROBABILITY
    ):
        if random.choices(
                (True, False),
                weights=(death_probability, 1 - death_probability)
        )[0]:
            return

        if self.age(condition.date).days >= 45:
            fattening_rabbit = FatteningRabbitFuture(status=set(), **self.__dict__)
            condition.add_fattening_rabbit(fattening_rabbit)
        else:
            condition.add_bunny(BunnyFuture(
                status={BunnyManager.STATUS_MOTHER_FEEDS}, **self.__dict__
            ))


class FatteningRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        pass


class MotherRabbitFuture(BaseRabbitFuture):
    DEFAULT_FERTILIZATION_PROBABILITY: Final[float] = 0.95
    DEFAULT_BIRTHS_PROBABILITY_MAP: Final[dict[int, float]] = {
        8: 1
    }

    def __init__(self, last_fertilization: date, last_births: date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_fertilization: Final[Optional[date]] = last_fertilization
        self.last_births: Final[Optional[date]] = last_births

    def tomorrow_state(
            self, condition, birth_probability_map: dict[int, float] = None,
            fertilization_probability: float = DEFAULT_FERTILIZATION_PROBABILITY
    ):
        if birth_probability_map is None:
            birth_probability_map = self.DEFAULT_BIRTHS_PROBABILITY_MAP

        if self.age(condition.date).days < 150:
            condition.add_mother_rabbit(MotherRabbitFuture(status=set(), **self.__dict__))
        else:
            pass
            # TODO: to determine status and offspring


class FatherRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        if self.age(condition.date).days >= 180:
            condition.add_father_rabbit(FatherRabbitFuture(
                status={
                    FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION,
                    FatherRabbitManager.STATUS_RESTING
                },
                **self.__dict__
            ))
        else:
            condition.add_father_rabbit(FatherRabbitFuture(
                status={FatherRabbitManager.STATUS_RESTING},
                **self.__dict__
            ))
