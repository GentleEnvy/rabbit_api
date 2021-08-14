from unittest import mock

from django.test import TestCase

from api.models import *
from api.services.model.task.controllers import *
from api.tests.factories import *

fp = 'model/task/anonymous/create'


class CreateBunnyJiggingTask(TestCase):
    fixtures = ['init/breed', f'{fp}/bunny_jigging']
    
    def test__suc(self):
        with mock.patch(
            'api.services.model.rabbit.managers._manager.BunnyManager.status',
            mock.PropertyMock(return_value={Bunny.Manager.STATUS_NEED_JIGGING})
        ):
            BunnyJiggingTaskController().update_anonymous()
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.CHAR_TYPE, BunnyJiggingTask.CHAR_TYPE)
        self.assertEqual(task.cage_from, MotherCage.objects.get())
    
    def test__err(self):
        BunnyJiggingTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 0)


class CreateVaccinationTask(TestCase):
    fixtures = ['init/breed', f'{fp}/vaccination']
    
    def test__suc(self):
        VaccinationTaskController().update_anonymous()
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.CHAR_TYPE, VaccinationTask.CHAR_TYPE)
        self.assertEqual(task.cage, FatteningCage.objects.get())
    
    def test__err(self):
        FatteningRabbit.objects.update(id=1, is_vaccinated=True)
        self.assertEqual(Task.objects.count(), 0)


class CreateSlaughterInspectionTask(TestCase):
    def setUp(self):
        self.cage = FatteningCageFactory()
        FatteningRabbitFactory.create_batch(5, is_male=True, cage=self.cage)
    
    def test__suc(self):
        with mock.patch(
            'api.services.model.rabbit.managers._manager.FatteningRabbitManager.status',
            mock.PropertyMock(
                return_value={FatteningRabbit.Manager.STATUS_NEED_INSPECTION}
            )
        ):
            SlaughterInspectionTaskController().update_anonymous()
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.CHAR_TYPE, SlaughterInspectionTask.CHAR_TYPE)
        self.assertEqual(task.cage, self.cage)
