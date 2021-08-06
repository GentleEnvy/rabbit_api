from typing import Final

from django.core.exceptions import ValidationError

import api.models as models
from api.services.model.rabbit.managers import *


class RabbitCleaner:
    def __init__(self, rabbit):
        self.rabbit: Final['models.Rabbit'] = rabbit
    
    def clean(self):
        pass


class DeadRabbitCleaner(RabbitCleaner):
    def clean(self):
        pass


class FatteningRabbitCleaner(RabbitCleaner):
    rabbit: 'models.FatteningRabbit'
    
    def clean(self):
        super().clean()
        if self.rabbit.is_male is None:
            raise ValidationError('The sex of the FatteningRabbit must be determined')
        if self.rabbit.plan is not None:
            self.for_plan()
    
    def for_plan(self):
        READY_TO_SLAUGHTER = FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER
        if READY_TO_SLAUGHTER not in self.rabbit.manager.status:
            raise ValidationError(
                'The fattening rabbit in the plan must have the status READY_TO_SLAUGHTER'
            )


class BunnyCleaner(RabbitCleaner):
    def clean(self):
        pass


class MotherRabbitCleaner(RabbitCleaner):
    def clean(self):
        super().clean()
        if self.rabbit.is_male is None:
            raise ValidationError('The sex of the MotherRabbit must be determined')
        if self.rabbit.is_male:
            raise ValidationError('MotherRabbit must be a female')
    
    def for_mating(self):
        if self.rabbit.current_type != models.Rabbit.TYPE_MOTHER:
            raise ValidationError('The rabbit is not mother')
        mother_status = self.rabbit.manager.status
        READY_FOR_FERTILIZATION = MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in mother_status:
            raise ValidationError('The female is not ready for fertilization')
        # MAYBE: forbid mating with STATUS_FEEDS_BUNNY
        CONFIRMED_PREGNANT = MotherRabbitManager.STATUS_CONFIRMED_PREGNANT
        if CONFIRMED_PREGNANT in mother_status:
            raise ValidationError('The female already pregnancy (confirmed)')


class FatherRabbitCleaner(RabbitCleaner):
    def clean(self):
        super().clean()
        if self.rabbit.is_male is None:
            raise ValidationError('The sex of the FatherRabbit must be determined')
        if not self.rabbit.is_male:
            raise ValidationError('FatherRabbit must be a male')
    
    def for_mating(self):
        if self.rabbit.current_type != models.Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not father')
        READY_FOR_FERTILIZATION = FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in self.rabbit.manager.status:
            raise ValidationError('The male is not ready for fertilization')
