from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager

from api.managers import *
from api.models._cages import *
from api.models._rabbits import *
from api.models.base import BaseModel

__all__ = [
    'Task', 'ToReproductionTask', 'SlaughterTask', 'MatingTask', 'BunnyJiggingTask',
    'VaccinationTask', 'SlaughterInspectionTask', 'FatteningSlaughterTask'
]


class Task(BaseModel):
    objects = InheritanceManager()
    
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.completed_at is not None:
            if self.user is None:
                raise ValidationError(
                    'The task cannot be completed until the user is specified'
                )
        else:  # completed_at is None
            if self.is_confirmed is not None:
                raise ValidationError("Can't confirm an uncompleted task")


class ToReproductionTask(Task):
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.CASCADE)
    cage_to = models.ForeignKey(Cage, on_delete=models.CASCADE, null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.rabbit.current_type != Rabbit.TYPE_FATTENING:
            raise ValidationError('The rabbit type is not a FatteningRabbit')
        if self.rabbit.is_male is None:
            raise ValidationError(
                'The sex of the rabbit changing the type must be determined'
            )
    
    def clean_cage_to(self):
        if self.cage_to is not None:
            self.cage_to.full_clean()
            if self.rabbit.is_male:
                if self.cage_to.cast.CHAR_TYPE == MotherCage.CHAR_TYPE:
                    raise ValidationError('The male cannot be jigged to MotherCage')
            else:  # rabbit is female
                if self.cage_to.cast.CHAR_TYPE == FatteningCage.CHAR_TYPE:
                    raise ValidationError('The female cannot be jigged to FatteningCage')


class SlaughterTask(Task):
    rabbit = models.ForeignKey(Rabbit, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        if self.rabbit.current_type == Rabbit.TYPE_DIED:
            raise ValidationError("Can't kill a dead rabbit")


class MatingTask(Task):
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.CASCADE)
    father_rabbit = models.ForeignKey(FatherRabbit, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        if self.mother_rabbit.current_type == Rabbit.TYPE_MOTHER:
            raise ValidationError('This rabbit is not mother')
        if self.father_rabbit.current_type == Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not father')
        
        mother_status = self.mother_rabbit.manager.status
        READY_FOR_FERTILIZATION = MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in mother_status:
            raise ValidationError('The female is not ready for fertilization')
        # MAYBE: forbid mating with STATUS_FEEDS_BUNNY
        CONFIRMED_PREGNANT = MotherRabbitManager.STATUS_CONFIRMED_PREGNANT
        if CONFIRMED_PREGNANT not in mother_status:
            raise ValidationError('The female already pregnancy (confirmed)')
        
        READY_FOR_FERTILIZATION = FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in self.father_rabbit.manager.status:
            raise ValidationError('The male is not ready for fertilization')


class BunnyJiggingTask(Task):
    cage_from = models.ForeignKey(MotherCage, on_delete=models.CASCADE)
    male_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_male_set'
    )
    female_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_female_set'
    )
    
    def clean(self):
        super().clean()
        bunny_set = self.__bunny_set()
        if bunny_set.count() == 0:
            raise ValidationError('There are no bunnies in cage_form')
        for bunny in bunny_set.all():
            if BunnyManager.STATUS_NEED_JIGGING not in bunny.manager.status:
                raise ValidationError(
                    "There is bunny in this cage that don't need jigging"
                )
    
    def clean_male_cage_to(self):
        if self.male_cage_to is not None:
            self.male_cage_to.clean_for_jigging_rabbits(
                self.__bunny_set().filter(is_male=True)
            )
    
    def clean_female_cage_to(self):
        if self.female_cage_to is not None:
            self.female_cage_to.clean_for_jigging_rabbits(
                self.__bunny_set().filter(is_male=False)
            )
    
    def __bunny_set(self):
        return self.cage_from.bunny_set.filter(current_type=Rabbit.TYPE_BUNNY)


# MAYBE: add vaccination tasks for father and mother rabbits
class VaccinationTask(Task):
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        fattening_set = self.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        if fattening_set.count() == 0:
            raise ValidationError('There are no fattening rabbits in cage')
        for fattening_rabbit in fattening_set.all():
            if fattening_rabbit.is_vaccinated:
                raise ValidationError('This rabbit already been vaccinated')


# TODO: take into account the additional feed
class SlaughterInspectionTask(Task):
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        fattening_set = self.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        if fattening_set.count() == 0:
            raise ValidationError('There is no fattening rabbit in this cage')
        NEED_INSPECTION = FatteningRabbitManager.STATUS_NEED_INSPECTION
        for fattening_rabbit in fattening_set:
            if NEED_INSPECTION not in fattening_rabbit.manager.status:
                raise ValidationError(
                    "There is fattening rabbit in this cage that don't need inspection"
                )


class FatteningSlaughterTask(Task):
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        fattening_set = self.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        if fattening_set.count() == 0:
            raise ValidationError('There are no fattening rabbits in this cage')
        for fattening_rabbit in fattening_set.all():
            READY_TO_SLAUGHTER = FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER
            if READY_TO_SLAUGHTER not in fattening_rabbit.cast.manager.status:
                raise ValidationError(
                    "There is fattening rabbit in this cage that don't ready to slaughter"
                )
