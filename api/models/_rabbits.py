from __future__ import annotations

from datetime import datetime
from typing import Final, Union

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from model_utils.managers import QueryManager
from multiselectfield import MultiSelectField

from api.managers.mixins import *
from api.models._plans import Plan
from api.models._breed import *
from api.models._history import *
from api.models.base import BaseHistoricalModel
from api.models._cages import *

__all__ = [
    'Rabbit', 'DeadRabbit', 'FatteningRabbit', 'Bunny', 'MotherRabbit', 'FatherRabbit'
]

_is_valid_cage = {'status': []}


class Rabbit(RabbitManagerMixin, BaseHistoricalModel):
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
            raise NotImplementedError("Instance can't be cast to Rabbit (base class)")
        if cls.CHAR_TYPE is None:
            raise NotImplementedError('CHAR_TYPE must be determined')
        if rabbit.current_type == DeadRabbit.CHAR_TYPE:
            raise TypeError("It's forbidden to recast from DeadRabbit")
        casted_rabbit = getattr(
            rabbit, cls.__name__.lower(), None
        ) or cls(rabbit_ptr=rabbit)
        casted_rabbit.__dict__.update(rabbit.__dict__)
        casted_rabbit.current_type = cls.CHAR_TYPE
        return casted_rabbit
    
    @property
    def cast(self) -> Union[DeadRabbit, _RabbitInCage]:
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
            raise NotImplementedError("Instance can't be saved as Rabbit (base class)")
        super().save(*args, **kwargs)


class DeadRabbit(Rabbit):
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


class _RabbitInCage(Rabbit):
    class Meta(Rabbit.Meta):
        abstract = True
    
    cage: Cage
    
    def get_absolute_url(self):
        raise NotImplementedError


class FatteningRabbit(FatteningRabbitManagerMixin, _RabbitInCage):
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
    
    def clean(self):
        super().clean()
        if self.is_male is None:
            raise ValidationError('The sex of the FatteningRabbit must be determined')
        if self.plan is not None:
            self.clean_for_plan()
    
    def clean_for_plan(self):
        from api.managers import FatteningRabbitManager
        READY_TO_SLAUGHTER = FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER
        if READY_TO_SLAUGHTER not in self.manager.status:
            raise ValidationError(
                'The fattening rabbit in the plan must have the status READY_TO_SLAUGHTER'
            )


class Bunny(BunnyManagerMixin, _RabbitInCage):
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


class MotherRabbit(MotherRabbitManagerMixin, _RabbitInCage):
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
    
    def clean(self):
        super().clean()
        if self.is_male is None:
            raise ValidationError('The sex of the MotherRabbit must be determined')
        if self.is_male:
            raise ValidationError('MotherRabbit must be a female')


class FatherRabbit(FatherRabbitManagerMixin, _RabbitInCage):
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
    
    def clean(self):
        super().clean()
        if self.is_male is None:
            raise ValidationError('The sex of the FatherRabbit must be determined')
        if not self.is_male:
            raise ValidationError('FatherRabbit must be a male')
