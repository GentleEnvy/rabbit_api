from abc import ABC
from datetime import date, timedelta
from typing import Final, Optional
import random

from api.services.forecast.rabbit._condition import ForecastCondition
from api.utils.functions import diff_time

__all__ = [
    'BaseRabbitFuture', 'BunnyFuture', 'FatteningRabbitFuture', 'MotherRabbitFuture',
    'FatherRabbitFuture'
]


class BaseRabbitFuture(ABC):
    def __init__(self, birthdate: date, status: str, id: int = None, **_):
        self.id: Final[Optional[int]] = id
        self.birthdate: Final[date] = birthdate
        self.status: Final[str] = status

    @property
    def age(self) -> timedelta:
        return diff_time(self.birthdate)

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

        if self.age.days >= 45:
            fattening_rabbit = FatteningRabbitFuture(**self.__dict__)
            condition.add_fattening_rabbit(fattening_rabbit)
        else:
            condition.add_bunny(self)


class FatteningRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        pass


class MotherRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        pass


class FatherRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        pass
