from abc import abstractmethod
from datetime import timedelta, date, datetime
from typing import Optional

from django.db.models import Q

from api.utils.functions import diff_time, to_datetime
from api import models as models

__all__ = [
    'RabbitManager', 'FatteningRabbitManager', 'BunnyManager',
    'MotherRabbitManager', 'FatherRabbitManager'
]


def _get_output(rabbit):
    children = rabbit.rabbit_set.all()
    if len(children) == 0:
        return 0
    births = [children[0].birthday]
    for child in children[1:]:
        for birth in births:
            if abs(diff_time(birth, child.birthday).days) > 2:
                births.append(child.birthday)
                break
    return len(births)


def _get_output_efficiency(rabbit, dead_causes):
    DeadRabbit = models.DeadRabbit
    efficiency_children = rabbit.rabbit_set.filter(
        ~Q(fatteningrabbit=None) | ~Q(motherrabbit=None) | ~Q(fatherrabbit=None) |
        Q(current_type=DeadRabbit.CHAR_TYPE) & ~Q(deadrabbit__death_cause__in=dead_causes)
    ).count()
    output = _get_output(rabbit)
    if output == 0:
        return None
    return efficiency_children / output


class RabbitManager:
    rabbit: 'models.Rabbit'
    
    def __init__(self, rabbit):
        self.rabbit = rabbit
    
    @property
    def age(self) -> timedelta:
        return diff_time(datetime.utcnow(), self.rabbit.birthday)
    
    @property
    @abstractmethod
    def status(self) -> set[str]:
        raise NotImplementedError


class FatteningRabbitManager(RabbitManager):
    rabbit: 'models.FatteningRabbit'
    
    STATUS_NEED_VACCINATION = 'NV'
    STATUS_NEED_INSPECTION = 'NI'
    STATUS_READY_TO_SLAUGHTER = 'RS'
    
    __NEED_INSPECTION_AGE = 80
    
    @property
    def status(self):
        if not self.rabbit.is_vaccinated:
            return {self.STATUS_NEED_VACCINATION}
        # vaccinated
        if self.age.days >= self.__NEED_INSPECTION_AGE:
            last_weighting = self.last_weighting
            if last_weighting is None:
                return {self.STATUS_NEED_INSPECTION}
            # last_weighting is not None
            if last_weighting < self.rabbit.birthday + timedelta(
                self.__NEED_INSPECTION_AGE
            ):
                return {self.STATUS_NEED_INSPECTION}
            # weighed later __NEED_INSPECTION_AGE
            return {self.STATUS_READY_TO_SLAUGHTER}
        # age < __NEED_INSPECTION_AGE
        return set()
    
    @property
    def last_weighting(self) -> Optional[datetime]:
        try:
            return models.FatteningRabbitHistory.objects.exclude(weight=None).filter(
                rabbit=self.rabbit
            ).latest('time').time
        except models.RabbitHistory.DoesNotExist:
            return None


class BunnyManager(RabbitManager):
    rabbit: 'models.Bunny'
    
    STATUS_NEED_JIGGING = 'NJ'
    
    __NEED_JIGGING_AGE = 45
    
    @property
    def status(self):
        if self.age.days >= self.__NEED_JIGGING_AGE:
            return {self.STATUS_NEED_JIGGING}
        return set()


class MotherRabbitManager(RabbitManager):
    rabbit: 'models.MotherRabbit'
    
    STATUS_READY_FOR_FERTILIZATION = 'RF'
    STATUS_UNCONFIRMED_PREGNANT = 'UP'
    STATUS_CONFIRMED_PREGNANT = 'CP'
    STATUS_FEEDS_BUNNY = 'FB'
    
    __READY_FOR_FERTILIZATION_AGE = 110
    
    @property
    def status(self):
        PregnancyInspection = models.PregnancyInspection
        statuses = set()
        
        rabbits_in_cage = self.rabbit.cage.manager.rabbits
        for rabbit_in_cage in rabbits_in_cage:
            if rabbit_in_cage != self.rabbit:
                if rabbit_in_cage.current_type == models.Bunny.CHAR_TYPE:
                    statuses.add(self.STATUS_FEEDS_BUNNY)
                    break
        
        if self.age.days < self.__READY_FOR_FERTILIZATION_AGE:
            return statuses
        
        # age >= __READY_FOR_FERTILIZATION_AGE
        last_births = self.last_births
        last_fertilization = self.last_fertilization
        if last_fertilization is None or diff_time(
            datetime.utcnow(), last_fertilization
        ).days >= 40:
            if last_births is None or to_datetime(
                last_births + timedelta(3)
            ) < datetime.utcnow():
                statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
            return statuses
        # last_fertilization is not None and isn't overdue
        if last_births is None or last_births < last_fertilization:
            try:
                last_pregnancy_inspection = PregnancyInspection.objects.filter(
                    mother_rabbit=self.rabbit, time__gte=last_fertilization
                ).latest('time')
            except PregnancyInspection.DoesNotExist:
                statuses.add(self.STATUS_UNCONFIRMED_PREGNANT)
                return statuses
            if last_pregnancy_inspection.is_pregnant:
                statuses.add(self.STATUS_CONFIRMED_PREGNANT)
            else:
                statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
            return statuses
        # last_births is not None and last_births > last_fertilization
        if to_datetime(last_births + timedelta(3)) > datetime.utcnow():
            statuses.add(self.STATUS_READY_FOR_FERTILIZATION)
        return statuses
    
    @property
    def last_births(self) -> Optional[date]:
        try:
            return models.Bunny.objects.filter(
                mother=self.rabbit
            ).latest('birthday').birthday
        except models.Bunny.DoesNotExist:
            return None
    
    @property
    def last_mating(self) -> Optional['models.Mating']:
        try:
            return models.Mating.objects.filter(
                mother_rabbit=self.rabbit
            ).latest('time')
        except models.Mating.DoesNotExist:
            return None
    
    @property
    def last_fertilization(self) -> Optional[datetime]:
        last_mating = self.last_mating
        if last_mating is None:
            return None
        return last_mating.time
    
    @property
    def output(self) -> int:
        # noinspection PyTypeChecker
        return _get_output(self.rabbit)
    
    @property
    def output_efficiency(self) -> Optional[float]:
        # noinspection PyTypeChecker
        return _get_output_efficiency(
            self.rabbit,
            (models.DeadRabbit.CAUSE_SLAUGHTER, models.DeadRabbit.CAUSE_EXTRA)
        )


class FatherRabbitManager(RabbitManager):
    rabbit: 'models.FatherRabbit'
    
    STATUS_READY_FOR_FERTILIZATION = 'RF'
    
    __READY_FOR_FERTILIZATION_AGE = 110
    
    @property
    def status(self):
        if self.age.days >= self.__READY_FOR_FERTILIZATION_AGE:
            return {self.STATUS_READY_FOR_FERTILIZATION}
        return set()
    
    @property
    def output(self) -> int:
        # noinspection PyTypeChecker
        return _get_output(self.rabbit)
    
    @property
    def output_efficiency(self) -> Optional[float]:
        # noinspection PyTypeChecker
        return _get_output_efficiency(
            self.rabbit,
            (models.DeadRabbit.CAUSE_ILLNESS, models.DeadRabbit.CAUSE_DISEASE)
        )
