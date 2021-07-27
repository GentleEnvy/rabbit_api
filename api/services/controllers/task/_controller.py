from typing import Callable, Type

from django.core.exceptions import ValidationError

from api.services.controllers.task.base import TaskController
from api.services.filterers.cage import CageFilterer
from api.models import *

__all__ = [
    'ToReproductionTaskController', 'SlaughterTaskController', 'MatingTaskController',
    'BunnyJiggingTaskController', 'VaccinationTaskController',
    'SlaughterInspectionTaskController', 'FatteningSlaughterTaskController'
]


def _setup_jigging_cage(
    task: Task, cage_from: Cage, cage_to_attr: str, cleaner: Callable,
    cage_to_type: Type[Cage] = None
) -> None:
    if getattr(task, cage_to_attr) is not None:
        try:
            cleaner()
            return
        except ValidationError:
            pass
    # noinspection SpellCheckingInspection
    filterer = CageFilterer(
        Cage.objects.select_related('fatteningcage', 'mothercage')
    )
    # TODO: check same cage
    for nearest_cage in filterer.order_by_nearest_to(cage_from, cage_to_type):
        setattr(task, cage_to_attr, nearest_cage)
        try:
            cleaner()
        except ValidationError:
            continue
        task.save()
        break
    # TODO: not valid cages


def _create_from_fattening_cage(controller, tasks):
    # noinspection SpellCheckingInspection
    for fattening_cage in FatteningCage.objects.exclude(
        id__in=[t.cage.id for t in tasks]
    ).prefetch_related('fatteningrabbit_set').all():
        try:
            controller.task_model.objects.create(cage=fattening_cage)
        except ValidationError:
            continue


class ToReproductionTaskController(TaskController):
    task_model = ToReproductionTask
    
    def _setup(self, tasks):
        for task in tasks:
            _setup_jigging_cage(task, task.rabbit.cage, 'cage_to', task.clean_cage_to)
    
    def execute(self, task: ToReproductionTask):
        rabbit = task.rabbit
        if rabbit.is_male:
            casted_rabbit = FatherRabbit.recast(rabbit)
        else:  # rabbit is female
            casted_rabbit = MotherRabbit.recast(rabbit)
        casted_rabbit.cage = task.cage_to.cast
        casted_rabbit.save()


class SlaughterTaskController(TaskController):
    task_model = SlaughterTask
    
    def execute(self, task: SlaughterTask):
        dead_rabbit = DeadRabbit.recast(task.rabbit)
        dead_rabbit.death_cause = DeadRabbit.CAUSE_SLAUGHTER
        dead_rabbit.save()


class MatingTaskController(TaskController):
    task_model = MatingTask
    
    def execute(self, task: MatingTask):
        Mating.objects.create(
            time=task.completed_at, mother_rabbit=task.mother_rabbit,
            father_rabbit=task.father_rabbit
        )


class BunnyJiggingTaskController(TaskController):
    task_model = BunnyJiggingTask
    
    def _create(self, tasks):
        for mother_cage in MotherCage.objects.exclude(
            id__in=[t.cage_from.id for t in tasks]
        ).prefetch_related('bunny_set').all():
            try:
                self.task_model.objects.create(cage_from=mother_cage)
            except ValidationError:
                continue
    
    def _setup(self, tasks):
        task: BunnyJiggingTask
        for task in tasks:
            _setup_jigging_cage(
                task, task.cage_from, 'male_cage_to', task.clean_male_cage_to,
                FatteningCage
            )
            _setup_jigging_cage(
                task, task.cage_from, 'female_cage_to', task.clean_female_cage_to,
                FatteningCage
            )
    
    def execute(self, task: BunnyJiggingTask):
        bunnies = task.cage_from.bunny_set.filter(current_type=Rabbit.TYPE_BUNNY)
        fattening_rabbits = list(map(FatteningRabbit.recast, bunnies))
        for male in fattening_rabbits[:task.males]:
            male.is_male = True
            male.cage = task.male_cage_to
        for female in fattening_rabbits[task.males:]:
            female.is_male = False
            female.cage = task.female_cage_to
        for fattening_rabbit in fattening_rabbits:
            fattening_rabbit.save()


class VaccinationTaskController(TaskController):
    task_model = VaccinationTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)
    
    def execute(self, task: VaccinationTask):
        fattening_rabbits = task.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        for fattening_rabbit in fattening_rabbits:
            fattening_rabbit.is_vaccinated = True
            fattening_rabbit.save()


class SlaughterInspectionTaskController(TaskController):
    task_model = SlaughterInspectionTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)
    
    def execute(self, task: SlaughterInspectionTask):
        weights = task.weights
        fattening_rabbits = task.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        for (weight, delay), fattening_rabbit in zip(weights.items(), fattening_rabbits):
            weight = float(weight)
            fattening_rabbit.weight = weight
            fattening_rabbit.save()
            if delay is not None:
                BeforeSlaughterInspection.objects.create(
                    rabbit=fattening_rabbit, time=task.completed_at, delay=delay
                )


class FatteningSlaughterTaskController(TaskController):
    task_model = FatteningSlaughterTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)
    
    def execute(self, task: FatteningSlaughterTask):
        fattening_rabbits = task.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        for fattening_rabbit in fattening_rabbits:
            dead_rabbit = DeadRabbit.recast(fattening_rabbit)
            dead_rabbit.death_cause = DeadRabbit.CAUSE_SLAUGHTER
            dead_rabbit.save()
