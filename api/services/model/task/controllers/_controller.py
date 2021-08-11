from datetime import datetime

from django.core.exceptions import ValidationError

from api.services.model.task.controllers.base import TaskController
from api.services.model.cage.filterer import CageFilterer
from api.models import *

__all__ = [
    'ToReproductionTaskController', 'ToFatteningTaskController', 'MatingTaskController',
    'BunnyJiggingTaskController', 'VaccinationTaskController',
    'SlaughterInspectionTaskController', 'SlaughterTaskController'
]


def _create_from_fattening_cage(controller, tasks):
    for fattening_cage in FatteningCage.objects.exclude(
        id__in=[t.cage.id for t in tasks]
    ):
        try:
            controller.task_model.objects.create(cage=fattening_cage)
        except ValidationError:
            continue


class ToReproductionTaskController(TaskController):
    task_model = ToReproductionTask
    
    def _setup(self, tasks):
        task: ToReproductionTask
        for task in tasks:
            if task.cage_to is not None:
                try:
                    task.full_clean()
                    continue
                except ValidationError:
                    pass
            filterer = CageFilterer(Cage.objects.select_subclasses())
            # TODO: check same cage
            is_found = False
            for nearest_cage in filterer.order_by_nearest_to(
                task.rabbit.cage, FatteningCage if task.rabbit.is_male else MotherCage
            ):
                try:
                    task.cage_to = nearest_cage
                    task.cleaner.clean_cage_to()
                    task.save()
                    is_found = True
                    break
                except ValidationError:
                    continue
            if not is_found:
                raise OverflowError('There are no suitable cages')
    
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
        task: ToFatteningTask
        for task in tasks:
            if task.cage_to is not None:
                try:
                    task.full_clean()
                    continue
                except ValidationError:
                    pass
            filterer = CageFilterer(Cage.objects.select_subclasses())
            # TODO: check same cage
            is_found = False
            for nearest_cage in filterer.order_by_nearest_to(
                task.rabbit.cast.cage, FatteningCage
            ):
                try:
                    task.cage_to = nearest_cage
                    task.cleaner.clean_cage_to()
                    task.save()
                    is_found = True
                    break
                except ValidationError:
                    continue
            if not is_found:
                raise OverflowError('There are no suitable cages')
    
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
        ):
            try:
                self.task_model.objects.create(cage_from=mother_cage)
            except ValidationError:
                continue
    
    def _setup(self, tasks):
        task: BunnyJiggingTask
        for task in tasks:
            if task.male_cage_to is not None:
                try:
                    task.full_clean()
                    continue
                except ValidationError:
                    pass
            filterer = CageFilterer(Cage.objects.select_subclasses())
            is_found_for_male = False
            is_found_for_female = False
            for nearest_cage in filterer.order_by_nearest_to(
                task.cage_from, FatteningCage
            ):
                if not is_found_for_male:
                    try:
                        task.male_cage_to = nearest_cage
                        task.cleaner.clean_male_cage_to()
                        is_found_for_male = True
                    except ValidationError:
                        continue
                else:
                    try:
                        task.female_cage_to = nearest_cage
                        task.cleaner.clean_female_cage_to()
                        is_found_for_female = True
                    except ValidationError:
                        continue
                if is_found_for_male and is_found_for_female:
                    try:
                        task.save()
                    except ValidationError:
                        is_found_for_male = False
                        is_found_for_female = False
                        continue
            if not is_found_for_male or not is_found_for_female:
                raise OverflowError('There are no suitable cages')
    
    def execute(self, task: BunnyJiggingTask):
        bunnies = task.cage_from.bunny_set.all()
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
        fattening_rabbits = task.cage.fatteningrabbit_set.all()
        for fattening_rabbit in fattening_rabbits:
            fattening_rabbit.is_vaccinated = True
            fattening_rabbit.save()


class SlaughterInspectionTaskController(TaskController):
    task_model = SlaughterInspectionTask
    
    def _create(self, tasks):
        _create_from_fattening_cage(self, tasks)
    
    def execute(self, task: SlaughterInspectionTask):
        fattening_rabbits = task.cage.fatteningrabbit_set.all()
        for rabbit, weight in zip(fattening_rabbits, task.weights):
            rabbit.weight = weight
            rabbit.last_weighting = datetime.utcnow()
            rabbit.save()


class SlaughterTaskController(TaskController):
    task_model = SlaughterTask
    
    def _create(self, tasks):
        exclude_rabbit_ids = [task.rabbit.id for task in tasks]
        for plan in Plan.objects.filter(date__lte=datetime.utcnow()):
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
