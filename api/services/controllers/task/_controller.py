from typing import Callable

from django.core.exceptions import ValidationError

from api.services.controllers.task.base import BaseTaskController
from api.services.filterers.cage import CageFilterer
from api.models import *

__all__ = [
    'ToReproductionTaskController', 'SlaughterTaskController', 'MatingTaskController',
    'BunnyJiggingTaskController', 'VaccinationTaskController',
    'SlaughterInspectionTaskController', 'FatteningSlaughterTaskController'
]


def _setup_jigging_cage(
    task: Task, cage_from: Cage, cage_to_attr: str, cleaner: Callable
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
    for nearest_cage in filterer.order_by_nearest_to(cage_from):
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


class ToReproductionTaskController(BaseTaskController):
    task_model = ToReproductionTask
    
    def _setup(self, tasks):
        for task in tasks:
            _setup_jigging_cage(task, task.rabbit.cage, 'cage_to', task.clean_cage_to)


class SlaughterTaskController(BaseTaskController):
    task_model = SlaughterTask


class MatingTaskController(BaseTaskController):
    task_model = MatingTask


class BunnyJiggingTaskController(BaseTaskController):
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
                task, task.cage_from, 'male_cage_to', task.clean_male_cage_to
            )
            _setup_jigging_cage(
                task, task.cage_from, 'female_cage_to', task.clean_female_cage_to
            )


class VaccinationTaskController(BaseTaskController):
    task_model = VaccinationTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)


class SlaughterInspectionTaskController(BaseTaskController):
    task_model = SlaughterInspectionTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)


class FatteningSlaughterTaskController(BaseTaskController):
    task_model = FatteningSlaughterTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)
