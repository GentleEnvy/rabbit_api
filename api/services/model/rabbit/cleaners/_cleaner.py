from typing import Final, Type

from django.core.exceptions import ValidationError

import api.models as models
from api.services.model.rabbit.managers import *

__all__ = [
    'RabbitCleaner', 'DeadRabbitCleaner', 'FatteningRabbitCleaner', 'BunnyCleaner',
    'MotherRabbitCleaner', 'FatherRabbitCleaner'
]


class RabbitCleaner:
    @classmethod
    def get_model(cls) -> Type['models.Rabbit']:
        return models.Rabbit
    
    @classmethod
    def check_type_of_rabbit(cls, rabbit, type_=None):
        type_ = type_ or cls.get_model()
        if not isinstance(rabbit, type_):
            raise ValidationError(
                f"Rabbit's type is {type(rabbit)} (not a {type_})"
            )
    
    def __init__(self, rabbit):
        self.rabbit: Final['models.Rabbit'] = rabbit
    
    def clean(self):
        pass
    
    def check_type(self):
        self.check_type_of_rabbit(self.rabbit)


class DeadRabbitCleaner(RabbitCleaner):
    @classmethod
    def get_model(cls) -> Type['models.DeadRabbit']:
        return models.DeadRabbit
    
    @classmethod
    def for_recast(cls, rabbit):
        if hasattr(rabbit, models.DeadRabbit.__name__.lower()):
            raise ValidationError("It's forbidden to recast from DeadRabbit")


class FatteningRabbitCleaner(RabbitCleaner):
    rabbit: 'models.FatteningRabbit'
    
    @classmethod
    def get_model(cls) -> Type['models.FatteningRabbit']:
        return models.FatteningRabbit
    
    @classmethod
    def for_recast(cls, rabbit):
        try:
            MotherRabbitCleaner.check_type_of_rabbit(rabbit)
        except ValidationError:
            FatherRabbitCleaner.check_type_of_rabbit(rabbit)
    
    def clean(self):
        super().clean()
        if self.rabbit.is_male is None:
            raise ValidationError('The sex of the FatteningRabbit must be determined')
        if self.rabbit.plan is not None:
            self.for_plan()
    
    def for_plan(self):
        # TODO: to plan cleaner (plan.cleaner.for_add_rabbit(self.rabbit))
        READY_TO_SLAUGHTER = FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER
        if READY_TO_SLAUGHTER not in self.rabbit.manager.status:
            raise ValidationError(
                'The fattening rabbit in the plan must have the status READY_TO_SLAUGHTER'
            )
    
    def for_recast_to_reproduction(self):
        if self.rabbit.is_male:
            FatherRabbitCleaner.for_recast(self.rabbit)
        else:  # rabbit is female
            MotherRabbitCleaner.for_recast(self.rabbit)
    
    def for_vaccinate(self):
        if self.rabbit.is_vaccinated:
            raise ValidationError('This rabbit already been vaccinated')
    
    def for_slaughter_inspection(self):
        NEED_INSPECTION = FatteningRabbitManager.STATUS_NEED_INSPECTION
        if NEED_INSPECTION not in self.rabbit.manager.status:
            raise ValidationError(
                "There is fattening rabbit in this cage that don't need inspection"
            )


class BunnyCleaner(RabbitCleaner):
    @classmethod
    def get_model(cls) -> Type['models.Bunny']:
        return models.Bunny
    
    def clean(self):
        super().clean()
        if self.rabbit.mother is None:
            raise ValidationError('The mother of the bunny must be determined')
        if self.rabbit.father is None:
            raise ValidationError('The father of the bunny must be determined')
    
    def for_jigging(self):
        self.check_type()
        if BunnyManager.STATUS_NEED_JIGGING not in self.rabbit.manager.status:
            raise ValidationError("This bunny don't need jigging")


class MotherRabbitCleaner(RabbitCleaner):
    @classmethod
    def get_model(cls) -> Type['models.MotherRabbit']:
        return models.MotherRabbit
    
    @classmethod
    def for_recast(cls, rabbit):
        FatteningRabbitCleaner.check_type_of_rabbit(rabbit)
        cls.check_rabbit(rabbit)
    
    @classmethod
    def check_rabbit(cls, rabbit):
        if rabbit.is_male is None:
            raise ValidationError('The sex of the MotherRabbit must be determined')
        if rabbit.is_male:
            raise ValidationError('MotherRabbit must be a female')
        if not rabbit.is_vaccinated:
            raise ValidationError('MotherRabbit must be vaccinated')
    
    def clean(self):
        super().clean()
        self.check_rabbit(self.rabbit)
    
    def for_mating(self):
        self.check_type()
        mother_status = self.rabbit.manager.status
        READY_FOR_FERTILIZATION = MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in mother_status:
            raise ValidationError('The female is not ready for fertilization')
        # MAYBE: forbid mating with STATUS_FEEDS_BUNNY
        CONFIRMED_PREGNANT = MotherRabbitManager.STATUS_CONFIRMED_PREGNANT
        if CONFIRMED_PREGNANT in mother_status:
            raise ValidationError('The female already pregnancy (confirmed)')
    
    def for_recast_to_fattening(self):
        FatteningRabbitCleaner.for_recast(self.rabbit)


class FatherRabbitCleaner(RabbitCleaner):
    @classmethod
    def get_model(cls) -> Type['models.FatherRabbit']:
        return models.FatherRabbit
    
    @classmethod
    def for_recast(cls, rabbit):
        FatteningRabbitCleaner.check_type_of_rabbit(rabbit)
        cls.check_rabbit(rabbit)
    
    @classmethod
    def check_rabbit(cls, rabbit):
        if rabbit.is_male is None:
            raise ValidationError('The sex of the FatherRabbit must be determined')
        if not rabbit.is_male:
            raise ValidationError('FatherRabbit must be a male')
        if not rabbit.is_vaccinated:
            raise ValidationError('FatherRabbit must be vaccinated')
    
    def clean(self):
        super().clean()
        self.check_rabbit(self.rabbit)
    
    def for_mating(self):
        if not isinstance(self.rabbit, models.FatherRabbit):
            raise ValidationError('This rabbit is not father')
        READY_FOR_FERTILIZATION = FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in self.rabbit.manager.status:
            raise ValidationError('The male is not ready for fertilization')
    
    def for_recast_to_fattening(self):
        FatteningRabbitCleaner.for_recast(self.rabbit)
