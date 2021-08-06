from __future__ import annotations

from datetime import datetime
from typing import Final

from django.db import models
from django.urls import reverse
from model_utils.managers import QueryManager
from multiselectfield import MultiSelectField

from api.models.base import BaseHistoricalModel
from api.models._plans import *
from api.models._breeds import *
from api.models._histories import *
from api.models._cages import *
from api.services.model.rabbit.cleaners.mixins import *
from api.services.model.rabbit.managers.mixins import *

__all__ = [
    'Rabbit', 'DeadRabbit', 'FatteningRabbit', 'Bunny', 'MotherRabbit', 'FatherRabbit'
]

_is_valid_cage = {'status': []}


class Rabbit(RabbitCleanerMixin, RabbitManagerMixin, BaseHistoricalModel):
    CHAR_TYPE: str = None
    
    history_model = RabbitHistory
    
    birthday = models.DateTimeField(default=datetime.utcnow)
    mother = models.ForeignKey(
        'MotherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    father = models.ForeignKey(
        'FatherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    is_male = models.BooleanField(null=True, blank=True)
    is_vaccinated = models.BooleanField(default=False)
    weight = models.FloatField(null=True, blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    current_type = models.CharField(
        choices=(
            (TYPE_DIED := 'D', 'TYPE_DEAD'),
            (TYPE_BUNNY := 'B', 'TYPE_BUNNY'),
            (TYPE_FATTENING := 'F', 'TYPE_FATTENING'),
            (TYPE_FATHER := 'P', 'TYPE_FATHER'),
            (TYPE_MOTHER := 'M', 'TYPE_MOTHER')
        ),
        max_length=1, default=TYPE_BUNNY
    )
    warning_status = MultiSelectField(
        choices=(
            (NOT_EAT := 'NE', 'NOT_EAT'),
            (NOT_DRINK := 'ND', 'NOT_DRINK'),
            (GOT_SICK := 'GS', 'GOT_SICK')
        ),
        blank=True, default='', max_choices=3
    )
    
    all_current: QueryManager
    
    @classmethod
    def recast(cls, rabbit: Rabbit):
        if cls is Rabbit:
            raise TypeError("Instance can't be cast to Rabbit (base class)")
        if cls.CHAR_TYPE is None:
            raise ValueError('CHAR_TYPE must be determined')
        DeadRabbit.Cleaner.for_recast(rabbit)
        
        casted_rabbit = getattr(rabbit, cls.__name__.lower(), None) or cls(
            rabbit_ptr=rabbit
        )
        casted_rabbit.__dict__.update(rabbit.__dict__)
        casted_rabbit.current_type = cls.CHAR_TYPE
        return casted_rabbit
    
    @property
    def cast(self):
        for rabbit_class in (
            DeadRabbit, FatteningRabbit, Bunny, MotherRabbit, FatherRabbit
        ):
            if self.current_type == rabbit_class.CHAR_TYPE:
                return getattr(self, rabbit_class.__name__.lower())
        raise AttributeError('Incorrect current_type')
    
    def get_absolute_url(self) -> str:
        raise NotImplementedError
    
    def save(self, *args, **kwargs):
        if self.__class__ is Rabbit:
            raise TypeError("Instance can't be saved as Rabbit (base class)")
        super().save(*args, **kwargs)


class DeadRabbit(DeadRabbitCleanerMixin, Rabbit):
    CHAR_TYPE: Final[str] = Rabbit.TYPE_DIED
    
    history_model = DeadRabbitHistory
    
    death_day = models.DateTimeField(default=datetime.utcnow)
    death_cause = models.CharField(
        choices=(
            (CAUSE_SLAUGHTER := 'S', 'CAUSE_SLAUGHTER'),
            (CAUSE_MOTHER := 'M', 'CAUSE_MOTHER'),
            (CAUSE_ILLNESS := 'I', 'CAUSE_ILLNESS'),
            (CAUSE_DISEASE := 'D', 'CAUSE_DISEASE'),
            (CAUSE_HEAT := 'H', 'CAUSE_HEAT'),
            (CAUSE_COOLING := 'C', 'CAUSE_COOLING'),
            (CAUSE_EXTRA := 'E', 'CAUSE_EXTRA')
        ),
        max_length=1
    )
    
    all_current = QueryManager(current_type=CHAR_TYPE)
    
    @classmethod
    def recast(cls, rabbit) -> DeadRabbit:
        return super().recast(rabbit)
    
    def get_absolute_url(self):
        raise AttributeError


class FatteningRabbit(FatteningRabbitCleanerMixin, FatteningRabbitManagerMixin, Rabbit):
    CHAR_TYPE: Final[str] = Rabbit.TYPE_FATTENING
    
    history_model = FatteningRabbitHistory
    
    cage = models.ForeignKey(
        FatteningCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    
    all_current = QueryManager(current_type=CHAR_TYPE)
    
    @classmethod
    def recast(cls, rabbit) -> FatteningRabbit:
        return super().recast(rabbit)
    
    def get_absolute_url(self):
        return reverse('fattening_rabbit__detail__url', kwargs={'id': self.id})


class Bunny(BunnyCleanerMixin, BunnyManagerMixin, Rabbit):
    CHAR_TYPE: Final[str] = Rabbit.TYPE_BUNNY
    
    history_model = BunnyHistory
    
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )
    
    all_current = QueryManager(current_type=CHAR_TYPE)
    
    @classmethod
    def recast(cls, _):
        raise NotImplementedError("It's forbidden to recast to Bunny")
    
    def get_absolute_url(self):
        return reverse('bunny__detail__url', kwargs={'id': self.id})


class MotherRabbit(MotherRabbitCleanerMixin, MotherRabbitManagerMixin, Rabbit):
    CHAR_TYPE: Final[str] = Rabbit.TYPE_MOTHER
    
    history_model = MotherRabbitHistory
    
    cage = models.ForeignKey(
        MotherCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )
    
    all_current = QueryManager(current_type=CHAR_TYPE)
    
    @classmethod
    def recast(cls, rabbit) -> MotherRabbit:
        return super().recast(rabbit)
    
    def get_absolute_url(self):
        return reverse('mother_rabbit__detail__url', kwargs={'id': self.id})


class FatherRabbit(FatherRabbitCleanerMixin, FatherRabbitManagerMixin, Rabbit):
    CHAR_TYPE: Final[str] = Rabbit.TYPE_FATHER
    
    history_model = FatherRabbitHistory
    
    cage = models.ForeignKey(
        FatteningCage, on_delete=models.PROTECT, limit_choices_to=_is_valid_cage
    )
    
    all_current = QueryManager(current_type=CHAR_TYPE)
    
    @classmethod
    def recast(cls, rabbit) -> FatherRabbit:
        return super().recast(rabbit)
    
    def get_absolute_url(self):
        return reverse('father_rabbit__detail__url', kwargs={'id': self.id})
