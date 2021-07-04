from copy import deepcopy
from datetime import date
from typing import Final

from api.services.forecast.rabbit._futures import *

__all__ = ['ForecastCondition']


class ForecastCondition:
    def __init__(
            self,
            date_: date,
            bunnies: set[BunnyFuture] = None,
            fattening_rabbits: set[FatteningRabbitFuture] = None,
            mother_rabbits: set[MotherRabbitFuture] = None,
            father_rabbits: set[FatherRabbitFuture] = None
    ):
        self.date: Final[date] = date_
        self.bunnies: Final[set[BunnyFuture]] = deepcopy(bunnies) or set()
        self.fattening_rabbits: Final[set[FatteningRabbitFuture]] = deepcopy(
            fattening_rabbits
        ) or set()
        self.mother_rabbits: Final[set[MotherRabbitFuture]] = deepcopy(
            mother_rabbits
        ) or set()
        self.father_rabbits: Final[set[FatherRabbitFuture]] = deepcopy(
            father_rabbits
        ) or set()

    def add_bunny(self, bunny: BunnyFuture) -> None:
        self.bunnies.add(deepcopy(bunny))

    def add_fattening_rabbit(self, fattening_rabbit: FatteningRabbitFuture) -> None:
        self.fattening_rabbits.add(deepcopy(fattening_rabbit))

    def add_mother_rabbit(self, mother_rabbit: MotherRabbitFuture) -> None:
        self.mother_rabbits.add(deepcopy(mother_rabbit))

    def add_father_rabbit(self, father_rabbit: FatherRabbitFuture) -> None:
        self.father_rabbits.add(deepcopy(father_rabbit))
