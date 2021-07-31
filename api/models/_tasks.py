from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager

from api.managers import *
from api.models._cages import *
from api.models._rabbits import *
from api.models.base import BaseModel

__all__ = [
    'Task', 'ToReproductionTask', 'ToFatteningTask', 'MatingTask', 'BunnyJiggingTask',
    'VaccinationTask', 'SlaughterInspectionTask', 'SlaughterTask'
]


class Task(BaseModel):
    objects = InheritanceManager()
    
    CHAR_TYPE: str
    
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
    CHAR_TYPE = 'R'
    
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.CASCADE)
    # in progress
    cage_to = models.ForeignKey(Cage, on_delete=models.CASCADE, null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.rabbit.current_type != Rabbit.TYPE_FATTENING:
            raise ValidationError('The rabbit type is not a FatteningRabbit')
        if self.rabbit.is_male is None:
            raise ValidationError(
                'The sex of the rabbit changing the type must be determined'
            )
        if self.cage_to is not None:
            self.clean_cage_to()
    
    def clean_cage_to(self):
        # TODO: check that the cage is not occupied by another task
        if self.rabbit.is_male:
            if self.cage_to.cast.CHAR_TYPE == MotherCage.CHAR_TYPE:
                raise ValidationError('The male cannot be jigged to MotherCage')
        else:  # rabbit is female
            if self.cage_to.cast.CHAR_TYPE == FatteningCage.CHAR_TYPE:
                raise ValidationError('The female cannot be jigged to FatteningCage')
        for neighbour in self.cage_to.cast.rabbits:
            if neighbour != self.rabbit:
                raise ValidationError(
                    'The cage for the reproduction rabbit must be empty'
                )


class ToFatteningTask(Task):
    CHAR_TYPE = 'F'
    
    rabbit = models.ForeignKey(Rabbit, on_delete=models.CASCADE)
    # in progress
    cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE, null=True, blank=True
    )
    
    def clean(self):
        super().clean()
        if self.rabbit.current_type not in (Rabbit.TYPE_MOTHER, Rabbit.TYPE_FATHER):
            raise ValidationError('The rabbit type is not a MotherRabbit or FatherRabbit')
        if self.cage_to is not None:
            self.clean_cage_to()
    
    def clean_cage_to(self):
        for neighbour in self.cage_to.cast.rabbits:
            if neighbour.is_male != self.rabbit.is_male:
                raise ValidationError(
                    'Fattening rabbits in the same cage must be of the same sex'
                )
            if neighbour.is_vaccinated != self.rabbit.is_vaccinated:
                raise ValidationError(
                    'Fattening rabbits in the same cage must have the same status of '
                    'vaccinated'
                )


class MatingTask(Task):
    CHAR_TYPE = 'M'
    
    mother_rabbit = models.ForeignKey(MotherRabbit, on_delete=models.CASCADE)
    father_rabbit = models.ForeignKey(FatherRabbit, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        self.clean_mother_rabbit(self.mother_rabbit)
        self.clean_father_rabbit(self.father_rabbit)
        # TODO: check the uniqueness (mother_rabbit, father_rabbit) for
        #   anonymous | in_progress
    
    @classmethod
    def clean_mother_rabbit(cls, mother_rabbit: MotherRabbit):
        if mother_rabbit.current_type != Rabbit.TYPE_MOTHER:
            raise ValidationError('The mother rabbit is not mother')
        mother_status = mother_rabbit.manager.status
        READY_FOR_FERTILIZATION = MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in mother_status:
            raise ValidationError('The female is not ready for fertilization')
        # MAYBE: forbid mating with STATUS_FEEDS_BUNNY
        CONFIRMED_PREGNANT = MotherRabbitManager.STATUS_CONFIRMED_PREGNANT
        if CONFIRMED_PREGNANT in mother_status:
            raise ValidationError('The female already pregnancy (confirmed)')
    
    @classmethod
    def clean_father_rabbit(cls, father_rabbit: FatherRabbit):
        if father_rabbit.current_type != Rabbit.TYPE_FATHER:
            raise ValidationError('This rabbit is not father')
        READY_FOR_FERTILIZATION = FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        if READY_FOR_FERTILIZATION not in father_rabbit.manager.status:
            raise ValidationError('The male is not ready for fertilization')


# noinspection SpellCheckingInspection
class BunnyJiggingTask(Task):
    CHAR_TYPE = 'B'
    
    cage_from = models.ForeignKey(MotherCage, on_delete=models.CASCADE)
    # in progress
    male_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_male_set'
    )
    female_cage_to = models.ForeignKey(
        FatteningCage, on_delete=models.CASCADE,
        null=True, blank=True, related_name='bunnyjiggingtask_by_female_set'
    )
    males = models.PositiveSmallIntegerField(null=True, blank=True)
    
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
            if self.male_cage_to == self.female_cage_to:
                raise ValidationError('Males and females cannot sit in the same cage')
            self.male_cage_to.clean_for_jigging_bunnies(
                self.__bunny_set().filter(is_male=True)
            )
    
    def clean_female_cage_to(self):
        if self.female_cage_to is not None:
            if self.female_cage_to == self.male_cage_to:
                raise ValidationError('Females and males cannot sit in the same cage')
            self.female_cage_to.clean_for_jigging_bunnies(
                self.__bunny_set().filter(is_male=False)
            )
    
    def __bunny_set(self):
        return self.cage_from.bunny_set.filter(current_type=Rabbit.TYPE_BUNNY)


# MAYBE: add vaccination tasks for father and mother rabbits
class VaccinationTask(Task):
    CHAR_TYPE = 'V'
    
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


class SlaughterInspectionTask(Task):
    CHAR_TYPE = 'I'
    
    cage = models.ForeignKey(FatteningCage, on_delete=models.CASCADE)
    # in progress
    weights: list[float] = ArrayField(models.FloatField(), null=True, blank=True)
    
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
        if self.weights is not None:
            self.clean_weights(self.weights, __fattening_rabbits=fattening_set)
    
    def clean_weights(self, weights, __fattening_rabbits=None):
        if len(weights) == 0:
            raise ValidationError('Weights cannot be empty')
        if __fattening_rabbits is None:
            fattening_set = self.cage.fatteningrabbit_set.filter(
                current_type=Rabbit.TYPE_FATTENING
            )
        else:
            fattening_set = __fattening_rabbits
        if len(weights) != fattening_set.count():
            raise ValidationError(
                'The length of the list of weights must match the number of rabbits in '
                'the cage'
            )


class SlaughterTask(Task):
    CHAR_TYPE = 'S'
    
    rabbit = models.ForeignKey(FatteningRabbit, on_delete=models.CASCADE)
