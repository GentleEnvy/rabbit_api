from abc import abstractmethod
from datetime import datetime, timedelta

from api.managers.base import *
from api.models import *

__all__ = [
    'RabbitTimeManager', 'FatteningRabbitTimeManager', 'BunnyTimeManager',
    'MotherRabbitTimeManager', 'FatherRabbitTimeManager'
]


class RabbitTimeManager(BaseTimeManager):
    model: 'Rabbit'

    @property
    def age(self) -> timedelta:
        return self.time - datetime.combine(self.model.birthdate, datetime.min.time())

    @property
    @abstractmethod
    def status(self) -> set[str]:
        raise NotImplementedError


class FatteningRabbitTimeManager(RabbitTimeManager):
    model: 'FatteningRabbit'

    STATUS_NEED_VACCINATED = 'NV'
    STATUS_NEED_INSPECTION = 'NI'
    STATUS_FATTENING_SLAUGHTER = 'FS'  # FIXME: leave ?

    @property
    def status(self):
        statuses = set()
        if not self.model.is_vaccinated:
            return statuses.add(self.STATUS_NEED_VACCINATED)
        if self.age.days >= 80:
            return statuses.add(self.STATUS_NEED_INSPECTION)
        return statuses or {self.STATUS_FATTENING_SLAUGHTER}


class BunnyTimeManager(RabbitTimeManager):
    model: 'Bunny'

    STATUS_NEED_JIGGING = 'NJ'
    STATUS_MOTHER_FEEDS = 'MF'

    @property
    def status(self):
        if self.age.days >= 45:
            return {self.STATUS_NEED_JIGGING}
        return {self.STATUS_MOTHER_FEEDS}


class MotherRabbitTimeManager(RabbitTimeManager):
    model: 'MotherRabbit'

    @property
    def status(self):
        return set(self.model.status)


class FatherRabbitTimeManager(RabbitTimeManager):
    model: 'FatherRabbit'

    STATUS_RESTING = 'R'
    STATUS_MATING = 'M'  # FIXME: leave ?

    @property
    def status(self):
        neighbours = self.model.cage.rabbits
        if len(neighbours) == 0:
            return {self.STATUS_RESTING}
        return {self.STATUS_MATING}
