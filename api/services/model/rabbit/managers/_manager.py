from abc import abstractmethod
from datetime import *

from django.db.models import Q, Prefetch

from api.utils.functions import diff_time, to_datetime
from api import models as models

__all__ = [
    'RabbitManager', 'FatteningRabbitManager', 'BunnyManager',
    'MotherRabbitManager', 'FatherRabbitManager'
]


def _get_output(rabbit):
    children = rabbit.manager.children
    if len(children) == 0:
        return 0
    births = [children[0].birthday]
    for child in children[1:]:
        for birth in births:
            if abs(diff_time(birth, child.birthday).days) > 2:
                births.append(child.birthday)
                break
    return len(births)


# noinspection PyUnresolvedReferences
def _get_output_efficiency(rabbit, dead_causes):
    if (children := getattr(rabbit, 'children', None)) is None:
        if isinstance(rabbit, models.MotherRabbit):
            children = getattr(rabbit.motherrabbit, 'children', None)
        else:
            children = getattr(rabbit.fatherrabbit, 'children', None)
    
    if children is None:
        efficiency_children = rabbit.rabbit_set.filter(
            ~Q(fatteningrabbit=None) | ~Q(motherrabbit=None) | ~Q(fatherrabbit=None) |
            ~Q(deadrabbit=None) & ~Q(deadrabbit__death_cause__in=dead_causes)
        ).count()
    else:
        efficiency_children = 0
        for child in children:
            if isinstance(
                child, (models.FatteningRabbit, models.MotherRabbit, models.FatherRabbit)
            ):
                efficiency_children += 1
            elif isinstance(
                child, models.DeadRabbit
            ) and child.death_cause in dead_causes:
                efficiency_children += 1
    
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
            last_weighting = self.rabbit.last_weighting
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
    
    @classmethod
    def prefetch_children(cls, queryset=None):
        if queryset is None:
            queryset = models.MotherRabbit.objects.all()
        return queryset.prefetch_related(
            Prefetch(
                f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}'
                f'rabbit_set',
                queryset=models.Rabbit.objects.select_subclasses().order_by('birthday'),
                to_attr='children'
            )
        )
    
    @classmethod
    def prefetch_matings(cls, queryset=None):
        if queryset is None:
            queryset = models.MotherRabbit.objects.all()
        return queryset.prefetch_related(
            Prefetch(
                f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}'
                f'mating_set',
                queryset=models.Mating.objects.order_by('time'),
                to_attr='matings'
            )
        )
    
    @classmethod
    def prefetch_bunnies(cls, queryset=None):
        if queryset is None:
            queryset = models.MotherRabbit.objects.all()
        return queryset.select_related(
            f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}cage'
        ).prefetch_related(
            Prefetch(
                f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}'
                f'cage__bunny_set', to_attr='bunnies'
            )
        )
    
    @classmethod
    def prefetch_pregnancy_inspections(cls, queryset=None):
        if queryset is None:
            queryset = models.MotherRabbit.objects.all()
        return queryset.select_related(
            f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}cage'
        ).prefetch_related(
            Prefetch(
                f'{"motherrabbit__" if queryset.model is models.Rabbit else ""}'
                'pregnancyinspection_set',
                queryset=models.PregnancyInspection.objects.order_by('time'),
                to_attr='pregnancy_inspections'
            )
        )
    
    @property
    def status(self):
        statuses = set()
        
        if len(self.rabbit.cage.manager.bunnies):
            statuses.add(self.STATUS_FEEDS_BUNNY)
        
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
            last_pregnancy_inspection = None
            if (
                pregnancy_inspections := getattr(
                    self.rabbit, 'pregnancy_inspections', None
                )
            ) is not None:
                for pregnancy_inspection in pregnancy_inspections[::-1]:
                    if pregnancy_inspection.time >= last_fertilization:
                        last_pregnancy_inspection = pregnancy_inspection
                        break
            else:
                try:
                    last_pregnancy_inspection = \
                        self.rabbit.pregnancyinspection_set.filter(
                            time__gte=last_fertilization
                        ).latest('time')
                except models.PregnancyInspection.DoesNotExist:
                    last_pregnancy_inspection = None
            if last_pregnancy_inspection is None:
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
    def children(self):
        if (children := getattr(self.rabbit, 'children', None)) is None:
            # noinspection PyUnresolvedReferences
            if (children := getattr(self.rabbit.motherrabbit, 'children', None)) is None:
                try:
                    return self.rabbit.rabbit_set.select_subclasses().all()
                except models.Bunny.DoesNotExist:
                    return None
        return children
    
    @property
    def last_births(self) -> 'date | None':
        if (children := getattr(self.rabbit, 'children', None)) is None:
            # noinspection PyUnresolvedReferences
            if (children := getattr(self.rabbit.motherrabbit, 'children', None)) is None:
                try:
                    return self.rabbit.rabbit_set.latest('birthday').birthday
                except models.Rabbit.DoesNotExist:
                    return None
        try:
            return children[-1].birthday
        except IndexError:
            return None
    
    @property
    def last_mating(self) -> 'models.Mating | None':
        if (matings := getattr(self.rabbit, 'matings', None)) is None:
            # noinspection PyUnresolvedReferences
            if (matings := getattr(self.rabbit.motherrabbit, 'matings', None)) is None:
                try:
                    return self.rabbit.mating_set.latest('time')
                except models.Mating.DoesNotExist:
                    return None
        try:
            return matings[-1]
        except IndexError:
            return None
    
    @property
    def last_fertilization(self) -> 'datetime | None':
        last_mating = self.last_mating
        if last_mating is None:
            return None
        return last_mating.time
    
    @property
    def output(self) -> int:
        # noinspection PyTypeChecker
        return _get_output(self.rabbit)
    
    @property
    def output_efficiency(self) -> 'float | None':
        # noinspection PyTypeChecker
        return _get_output_efficiency(
            self.rabbit,
            (models.DeadRabbit.CAUSE_SLAUGHTER, models.DeadRabbit.CAUSE_EXTRA)
        )


class FatherRabbitManager(RabbitManager):
    rabbit: 'models.FatherRabbit'
    
    STATUS_READY_FOR_FERTILIZATION = 'RF'
    
    __READY_FOR_FERTILIZATION_AGE = 110
    
    @classmethod
    def prefetch_children(cls, queryset=None):
        if queryset is None:
            queryset = models.FatherRabbit.objects.all()
        queryset = queryset.prefetch_related(
            Prefetch(
                f'{"fatherrabbit__" if queryset.model is models.Rabbit else ""}'
                f'rabbit_set',
                queryset=models.Rabbit.objects.select_subclasses().order_by('birthday'),
                to_attr='children'
            )
        )
        return queryset
    
    @property
    def children(self):
        if (children := getattr(self.rabbit, 'children', None)) is None:
            # noinspection PyUnresolvedReferences
            if (children := getattr(self.rabbit.fatherrabbit, 'children', None)) is None:
                try:
                    return self.rabbit.rabbit_set.select_subclasses().all()
                except models.Rabbit.DoesNotExist:
                    return None
        return children
    
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
    def output_efficiency(self) -> 'float | None':
        # noinspection PyTypeChecker
        return _get_output_efficiency(
            self.rabbit,
            (models.DeadRabbit.CAUSE_ILLNESS, models.DeadRabbit.CAUSE_DISEASE)
        )
