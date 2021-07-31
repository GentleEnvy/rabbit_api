from datetime import datetime
from typing import Callable, Type

from django.core.exceptions import ValidationError

from api.services.controllers.task.base import TaskController
from api.services.filterers.cage import CageFilterer
from api.models import *

__all__ = [
    'ToReproductionTaskController', 'ToFatteningTaskController', 'MatingTaskController',
    'BunnyJiggingTaskController', 'VaccinationTaskController',
    'SlaughterInspectionTaskController', 'SlaughterTaskController'
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
        try:
            nearest_cage.clean_for_task()
            setattr(task, cage_to_attr, nearest_cage)
            cleaner()
        except ValidationError:
            continue
        task.save()
        break
    raise ValidationError('There are no suitable cages')


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


class ToFatteningTaskController(TaskController):
    task_model = ToFatteningTask
    
    def _setup(self, tasks):
        for task in tasks:
            _setup_jigging_cage(task, task.rabbit.cage, 'cage_to', task.clean_cage_to)
    
    def execute(self, task: ToReproductionTask):
        casted_rabbit = FatteningRabbit.recast(task.rabbit)
        casted_rabbit.cage = task.cage_to
        casted_rabbit.save()


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
        fattening_rabbits = task.cage.fatteningrabbit_set.filter(
            current_type=Rabbit.TYPE_FATTENING
        )
        for rabbit, weight in zip(fattening_rabbits, task.weights):
            rabbit.weight = weight
            rabbit.save()


class SlaughterTaskController(TaskController):
    task_model = SlaughterTask
    
    def _create(self, tasks):
        exclude_rabbit_ids = [task.rabbit.id for task in tasks]
        for plan in Plan.objects.prefetch_related('fatteningrabbit_set').filter(
            date__lte=datetime.utcnow()
        ).all():
            for fattening_rabbit in plan.fatteningrabbit_set.exclude(
                id__in=exclude_rabbit_ids
            ):
                try:
                    SlaughterTask.objects.create(rabbit=fattening_rabbit)
                except ValidationError:
                    continue
    
    def execute(self, task: SlaughterTask):
        dead_rabbit = DeadRabbit.recast(task.rabbit)
        dead_rabbit.death_cause = DeadRabbit.CAUSE_SLAUGHTER
        dead_rabbit.save()
