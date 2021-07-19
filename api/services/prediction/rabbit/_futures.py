from abc import ABC
from datetime import date, timedelta, datetime
from typing import Final, Optional, Union
import random

from api.managers import *
from api.services.prediction.rabbit import _condition as cond
from api.utils.functions import diff_time

__all__ = [
    'BaseRabbitFuture', 'BunnyFuture', 'FatteningRabbitFuture', 'MotherRabbitFuture',
    'FatherRabbitFuture'
]


class BaseRabbitFuture(ABC):
    def __init__(self, birthday: date, status: set[str], id: int = None, **_):
        self.id: Final[Optional[int]] = id
        self.birthday: Final[date] = birthday
        self.status: Final[set[str]] = status

    def age(self, target_date: Union[date, datetime]) -> timedelta:
        return diff_time(target_date, self.birthday)

    def tomorrow_state(self, condition: 'cond.PredictionCondition') -> None:
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
            fattening_rabbit = FatteningRabbitFuture(**self.__dict__ | {'status': set()})
            condition.add_fattening_rabbit(fattening_rabbit)
        else:
            condition.add_bunny(
                BunnyFuture(
                    **self.__dict__ | {'status': {BunnyManager.STATUS_MOTHER_FEEDS}}
                )
            )


class FatteningRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        if FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER in self.status:
            return

        fattening_status = set()
        age = self.age(condition.date).days
        if age >= 80:
            if age < 90:
                fattening_status.add(FatteningRabbitManager.STATUS_WITHOUT_COCCIDIOSTATIC)
            else:  # age >= 90
                fattening_status.add(FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER)
        # age < 80
        condition.add_fattening_rabbit(
            FatteningRabbitFuture(
                **self.__dict__ | {'status': fattening_status}
            )
        )


class MotherRabbitFuture(BaseRabbitFuture):
    DEFAULT_FERTILIZATION_PROBABILITY: Final[float] = 0.95
    DEFAULT_BIRTHS_PROBABILITY_MAP: Final[dict[int, float]] = {
        7: 0.3,
        8: 0.7
    }

    def __init__(self, last_fertilization: date, last_births: date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_fertilization: Final[Optional[date]] = last_fertilization
        self.last_births: Final[Optional[date]] = last_births

    def tomorrow_state(
        self, condition, birth_prob_map: dict[int, float] = None,
        fertilization_prob: float = DEFAULT_FERTILIZATION_PROBABILITY
    ):
        def _rand_birth_count() -> int:
            return random.choices(
                list(birth_prob_map.keys()), list(birth_prob_map.values())
            )[0]

        def _rand_was_fertilized() -> bool:
            return random.choices(
                (True, False), weights=(
                    fertilization_prob, 1 - fertilization_prob
                )
            )[0]

        if birth_prob_map is None:
            birth_prob_map = self.DEFAULT_BIRTHS_PROBABILITY_MAP

        mother_status = set()
        last_fertilization = self.last_fertilization
        last_births = self.last_births
        if self.age(condition.date).days >= 150:
            if MotherRabbitManager.STATUS_FEEDS_BUNNY in self.status:
                mother_status.add(MotherRabbitManager.STATUS_FEEDS_BUNNY)
            if MotherRabbitManager.STATUS_CONFIRMED_PREGNANT in self.status:
                if self.last_fertilization is not None:
                    if diff_time(condition.date, self.last_fertilization).days >= 29:
                        self._birth(condition, _rand_birth_count())
                        mother_status.add(MotherRabbitManager.STATUS_FEEDS_BUNNY)
                        last_births = condition.date
                    else:  # pregnancy duration < 29 days
                        mother_status.add(MotherRabbitManager.STATUS_CONFIRMED_PREGNANT)
                else:  # self.last_fertilization is None
                    last_births = condition.date
            else:  # female is not pregnant
                if MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION in self.status:
                    if _rand_was_fertilized():
                        last_fertilization = condition.date
                        mother_status.add(MotherRabbitManager.STATUS_CONFIRMED_PREGNANT)
                    else:  # female wasn't fertilized
                        mother_status.add(
                            MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
                        )
                else:  # female don't ready to fertilization
                    if self.last_births is not None:
                        if diff_time(condition.date, self.last_births).days > 3:
                            mother_status.add(
                                MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
                            )
                        # else: # less than 3 days have passed since the last pregnancy
                    else:  # self.last_births is None
                        mother_status.add(
                            MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
                        )

        condition.add_mother_rabbit(
            MotherRabbitFuture(
                **self.__dict__ | {
                    'status': mother_status,
                    'last_fertilization': last_fertilization,
                    'last_births': last_births
                }
            )
        )

    @staticmethod
    def _birth(condition: 'cond.PredictionCondition', count: int):
        for _ in range(count):
            condition.add_bunny(
                BunnyFuture(
                    birthday=condition.date,
                    status={BunnyManager.STATUS_MOTHER_FEEDS}
                )
            )


class FatherRabbitFuture(BaseRabbitFuture):
    def tomorrow_state(self, condition):
        if self.age(condition.date).days >= 180:
            condition.add_father_rabbit(
                FatherRabbitFuture(
                    **self.__dict__ | {
                        'status': {
                            FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION,
                            FatherRabbitManager.STATUS_RESTING
                        }
                    }
                )
            )
        else:
            condition.add_father_rabbit(
                FatherRabbitFuture(
                    **self.__dict__ | {'status': {FatherRabbitManager.STATUS_RESTING}}
                )
            )
