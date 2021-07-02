from abc import abstractmethod
from datetime import datetime, timedelta, date
from typing import Optional

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

    STATUS_NEED_VACCINATION = 'NV'
    STATUS_NEED_INSPECTION = 'NI'
    # noinspection SpellCheckingInspection
    STATUS_WITHOUT_COCCIDIOSTATIC = 'WC'
    STATUS_READY_TO_SLAUGHTER = 'RS'

    @property
    def status(self):
        if not self.model.is_vaccinated:
            return {self.STATUS_NEED_VACCINATION}
        # vaccinated
        if (age := self.age.days) >= 80:
            try:
                last_inspection = Inspection.objects.filter(
                    time__gte=self.model.birthdate + timedelta(80),
                    rabbit=self.model
                ).latest('time')
            except Inspection.DoesNotExist:
                return {self.STATUS_NEED_INSPECTION}
            # recently there was an inspection
            if last_inspection.delay is None:
                try:
                    last_inspection_with_delay = Inspection.objects.filter(
                        time__gte=self.model.birthdate + timedelta(80),
                        rabbit=self.model
                    ).exclude(delay=None).latest('time')
                except Inspection.DoesNotExist:
                    # not underweight
                    if age >= 90:
                        return {self.STATUS_READY_TO_SLAUGHTER}
                    return {self.STATUS_WITHOUT_COCCIDIOSTATIC}
                # was underweight
                if last_inspection_with_delay.time + timedelta(
                        last_inspection_with_delay.delay + 10
                ) > self.time:
                    return {self.STATUS_READY_TO_SLAUGHTER}
                return {self.STATUS_WITHOUT_COCCIDIOSTATIC}
            # is underweight
            if last_inspection.time + timedelta(last_inspection.delay) > self.time:
                return {self.STATUS_NEED_INSPECTION}
            # continue to fattening on delay
        # younger than 80 days
        return set()


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

    STATUS_READY_FOR_FERTILIZATION = 'RF'
    STATUS_PREGNANT = 'P'
    STATUS_FEEDS_BUNNY = 'FB'

    @property
    def last_births(self) -> Optional[date]:
        try:
            return Rabbit.objects.filter(
                mother__rabbit=self.model
            ).latest('birthdate').birthdate
        except Rabbit.DoesNotExist:
            return None

    @property
    def status(self):
        statuses = set()
        if self.model.is_pregnant:
            statuses.add(self.STATUS_PREGNANT)
        elif self.age.days >= 150 and self.last_births + timedelta(3) > self.time:
            statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
        rabbits_in_cage = self.model.cage.cast.rabbits
        if len(rabbits_in_cage) > 1:
            statuses.add(self.STATUS_FEEDS_BUNNY)
        return statuses


class FatherRabbitTimeManager(RabbitTimeManager):
    model: 'FatherRabbit'

    STATUS_READY_FOR_FERTILIZATION = 'RF'
    STATUS_RESTING = 'R'

    @property
    def status(self):
        statuses = set()
        if self.age.days >= 180:
            statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
        rabbits_in_cage = self.model.cage.cast.rabbits
        if len(rabbits_in_cage) == 1:
            statuses.add(self.STATUS_RESTING)
        return statuses
