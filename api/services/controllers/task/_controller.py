from datetime import date

from django.core.exceptions import ValidationError

from api.services.controllers.task.base import BaseTaskController
from api.models import *

__all__ = [
    'ToReproductionTaskController', 'SlaughterTaskController', 'MatingTaskController',
    'BunnyJiggingTaskController', 'VaccinationTaskController',
    'SlaughterInspectionTaskController', 'FatteningSlaughterTaskController'
]


class ToReproductionTaskController(BaseTaskController):
    task_model = ToReproductionTask


class SlaughterTaskController(BaseTaskController):
    task_model = SlaughterTask


class MatingTaskController(BaseTaskController):
    task_model = MatingTask


class BunnyJiggingTaskController(BaseTaskController):
    task_model = BunnyJiggingTask


class VaccinationTaskController(BaseTaskController):
    task_model = VaccinationTask


class SlaughterInspectionTaskController(BaseTaskController):
    task_model = SlaughterInspectionTask


class FatteningSlaughterTaskController(BaseTaskController):
    task_model = FatteningSlaughterTask
