from typing import Final

from django.core.exceptions import ValidationError
from django.db.models import Q

import api.models as models
from api.services.model.rabbit.cleaners import FatteningRabbitCleaner

__all__ = [
    'TaskCleaner', 'ToReproductionTaskCleaner', 'ToFatteningTaskCleaner',
    'MatingTaskCleaner', 'BunnyJiggingTaskCleaner', 'VaccinationTaskCleaner',
    'SlaughterInspectionTaskCleaner', 'SlaughterTaskCleaner'
]


class TaskCleaner:
    task: 'models.Task'
    
    def __init__(self, task):
        self.task: Final['models.Task'] = task
    
    def clean(self):
        if self.task.completed_at is not None:
            if self.task.user is None:
                raise ValidationError(
                    'The task cannot be completed until the user is specified'
                )
        else:  # completed_at is None
            if self.task.is_confirmed is not None:
                raise ValidationError("Can't confirm an uncompleted task")


class ToReproductionTaskCleaner(TaskCleaner):
    task: 'models.ToReproductionTask'
    
    def clean(self):
        super().clean()
        self.task.rabbit.cleaner.for_recast_to_reproduction()
        if self.task.cage_to is not None:
            self.clean_cage_to(True)
    
    def clean_cage_to(self, exclude_self=False):
        self.task.cage_to.cleaner.for_task(self.task if exclude_self else None)
        if self.task.rabbit.is_male:
            if self.task.cage_to.cast.CHAR_TYPE == models.MotherCage.CHAR_TYPE:
                raise ValidationError('The male cannot be jigged to MotherCage')
        else:  # rabbit is female
            if self.task.cage_to.cast.CHAR_TYPE == models.FatteningCage.CHAR_TYPE:
                raise ValidationError('The female cannot be jigged to FatteningCage')
        for neighbour in self.task.cage_to.manager.rabbits:
            if neighbour != self.task.rabbit:
                raise ValidationError(
                    'The cage for the reproduction rabbit must be empty'
                )


class ToFatteningTaskCleaner(TaskCleaner):
    task: 'models.ToFatteningTask'
    
    def clean(self):
        super().clean()
        FatteningRabbitCleaner.for_recast(self.task.rabbit)
        if self.task.cage_to is not None:
            self.clean_cage_to(True)
    
    def clean_cage_to(self, exclude_self=False):
        self.task.cage_to.cleaner.for_task(self.task if exclude_self else None)
        for neighbour in self.task.cage_to.cast.manager.rabbits:
            if neighbour.is_male != self.task.rabbit.is_male:
                raise ValidationError(
                    'Fattening rabbits in the same cage must be of the same sex'
                )
            if neighbour.is_vaccinated != self.task.rabbit.is_vaccinated:
                raise ValidationError(
                    'Fattening rabbits in the same cage must have the same status of '
                    'vaccinated'
                )


class MatingTaskCleaner(TaskCleaner):
    task: 'models.MatingTask'
    
    def clean(self):
        try:
            models.MatingTask.objects.exclude(id=self.task.id).get(
                Q(is_confirmed=None) &
                Q(mother_rabbit=self.task.mother_rabbit) |
                Q(father_rabbit=self.task.father_rabbit)
            )
            raise ValidationError('This rabbits is already waiting for mating')
        except models.MatingTask.DoesNotExist:
            super().clean()
            self.task.mother_rabbit.cleaner.for_mating()
            self.task.father_rabbit.cleaner.for_mating()
    
    @classmethod
    def check_exists(cls, rabbit):
        filters = {
            'is_confirmed': None,
            'father_rabbit' if rabbit.is_male else 'mother_rabbit': rabbit
        }
        if models.MatingTask.objects.filter(**filters).first() is not None:
            raise ValidationError('This rabbits is already waiting for mating')


class BunnyJiggingTaskCleaner(TaskCleaner):
    task: 'models.BunnyJiggingTask'
    
    def clean(self):
        super().clean()
        bunny_set = self.__bunny_set()
        if bunny_set.count() == 0:
            raise ValidationError('There are no bunnies in cage_from')
        
        is_bunny_need_jigging = False
        for bunny in bunny_set.all():
            try:
                bunny.cleaner.for_jigging()
            except ValidationError:
                continue
            is_bunny_need_jigging = True
            break
        if not is_bunny_need_jigging:
            raise ValidationError(
                "There are no bunnies in this cage that need jigging"
            )
        
        if self.task.male_cage_to is not None:
            self.clean_male_cage_to(True)
            if self.task.female_cage_to is None:
                raise ValidationError(
                    'male_cage_to is not None, but female_cage_to is None'
                )
            self.clean_female_cage_to(True)
        elif self.task.female_cage_to is not None:
            raise ValidationError(
                'female_cage_to is not None, but male_cage_to is None'
            )
    
    def clean_male_cage_to(self, exclude_self=False):
        self.task.male_cage_to.cleaner.for_task(self.task if exclude_self else None)
        if self.task.male_cage_to == self.task.female_cage_to:
            raise ValidationError('Males and females cannot sit in the same cage')
        self.task.male_cage_to.cleaner.for_jigging_bunnies(
            self.__bunny_set().filter(is_male=True)
        )
    
    def clean_female_cage_to(self, exclude_self=False):
        self.task.female_cage_to.cleaner.for_task(self.task if exclude_self else None)
        if self.task.female_cage_to == self.task.male_cage_to:
            raise ValidationError('Females and males cannot sit in the same cage')
        self.task.female_cage_to.cleaner.for_jigging_bunnies(
            self.__bunny_set().filter(is_male=False)
        )
    
    def __bunny_set(self):
        return self.task.cage_from.bunny_set.all()


class VaccinationTaskCleaner(TaskCleaner):
    task: 'models.VaccinationTask'
    
    def clean(self):
        super().clean()
        fattening_set = self.task.cage.fatteningrabbit_set.all()
        if fattening_set.count() == 0:
            raise ValidationError('There are no fattening rabbits in cage')
        for fattening_rabbit in fattening_set.all():
            fattening_rabbit.cleaner.for_vaccinate()


class SlaughterInspectionTaskCleaner(TaskCleaner):
    task: 'models.SlaughterInspectionTask'
    
    def clean(self):
        super().clean()
        fattening_set = self.task.cage.fatteningrabbit_set.all()
        if fattening_set.count() == 0:
            raise ValidationError('There is no fattening rabbit in this cage')
        
        needs = False
        for fattening_rabbit in fattening_set:
            try:
                fattening_rabbit.cleaner.for_slaughter_inspection()
                needs = True
                break
            except ValidationError:
                continue
        if not needs:
            raise ValidationError('No rabbit in this cage needs the inspection')
        
        if self.task.weights is not None:
            self.clean_weights(self.task.weights, _fattening_rabbits=fattening_set)
    
    def clean_weights(self, weights, _fattening_rabbits=None):
        if len(weights) == 0:
            raise ValidationError('Weights cannot be empty')
        if _fattening_rabbits is None:
            fattening_set = self.task.cage.fatteningrabbit_set.all()
        else:
            fattening_set = _fattening_rabbits
        if len(weights) != fattening_set.count():
            raise ValidationError(
                'The length of the list of weights must match the number of rabbits in '
                'the cage'
            )


class SlaughterTaskCleaner(TaskCleaner):
    task: 'models.SlaughterTask'
