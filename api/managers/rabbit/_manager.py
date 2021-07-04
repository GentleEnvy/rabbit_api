from abc import abstractmethod
from datetime import timedelta, date, datetime
from typing import Optional

from django.utils.timezone import now

from api.utils.functions import diff_time
from api.managers.base import *
from api import models as api_models

__all__ = [
    'RabbitManager', 'FatteningRabbitManager', 'BunnyManager',
    'MotherRabbitManager', 'FatherRabbitManager'
]


class RabbitManager(BaseManager):
    model: 'api_models.Rabbit'

    @property
    def age(self) -> timedelta:
        return diff_time(now(), self.model.birthdate)

    @property
    @abstractmethod
    def status(self) -> set[str]:
        raise NotImplementedError


class FatteningRabbitManager(RabbitManager):
    model: 'api_models.FatteningRabbit'

    STATUS_NEED_VACCINATION = 'NV'
    STATUS_NEED_INSPECTION = 'NI'
    # noinspection SpellCheckingInspection
    STATUS_WITHOUT_COCCIDIOSTATIC = 'WC'
    STATUS_READY_TO_SLAUGHTER = 'RS'

    @property
    def status(self):
        Inspection = api_models.Inspection
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
                ) > now():
                    return {self.STATUS_READY_TO_SLAUGHTER}
                return {self.STATUS_WITHOUT_COCCIDIOSTATIC}
            # is underweight
            if last_inspection.time + timedelta(last_inspection.delay) > now():
                return {self.STATUS_NEED_INSPECTION}
            # continue to fattening on delay
        # younger than 80 days
        return set()


class BunnyManager(RabbitManager):
    model: 'api_models.Bunny'

    STATUS_NEED_JIGGING = 'NJ'
    STATUS_MOTHER_FEEDS = 'MF'

    @property
    def status(self):
        if self.age.days >= 45:
            return {self.STATUS_NEED_JIGGING}
        return {self.STATUS_MOTHER_FEEDS}


class MotherRabbitManager(RabbitManager):
    model: 'api_models.MotherRabbit'

    STATUS_READY_FOR_FERTILIZATION = 'RF'
    STATUS_PREGNANT = 'P'
    STATUS_FEEDS_BUNNY = 'FB'

    @property
    def status(self):
        statuses = set()
        if self.model.is_pregnant:
            statuses.add(self.STATUS_PREGNANT)
        elif self.age.days >= 150 and self.last_births + timedelta(3) > now():
            statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
        rabbits_in_cage = self.model.cage.cast.rabbits
        if len(rabbits_in_cage) > 1:
            statuses.add(self.STATUS_FEEDS_BUNNY)
        return statuses

    @property
    def last_births(self) -> Optional[date]:
        try:
            return api_models.Rabbit.objects.filter(
                mother__rabbit=self.model
            ).latest('birthdate').birthdate
        except api_models.Rabbit.DoesNotExist:
            return None

    @property
    def last_fertilization(self) -> Optional[datetime]:
        try:
            return api_models.MotherRabbitHistory.objects.filter(
                rabbit=self.model, is_pregnant=True
            ).latest('time').time
        except api_models.MotherRabbitHistory.DoesNotExist:
            return None


class FatherRabbitManager(RabbitManager):
    model: 'api_models.FatherRabbit'

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
