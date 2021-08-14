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
    
    def test__fail(self):
        BunnyJiggingTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 0)


class CreateVaccinationTask(TestCase):
    fixtures = ['init/breed', f'{fp}/vaccination']
    
    def test__suc(self):
        VaccinationTaskController().update_anonymous()
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.CHAR_TYPE, VaccinationTask.CHAR_TYPE)
        self.assertEqual(task.cage, FatteningCage.objects.get())
    
    def test__fail(self):
        FatteningRabbit.objects.update(id=1, is_vaccinated=True)
        VaccinationTaskController().update_anonymous()
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
    
    def test__fail(self):
        SlaughterInspectionTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 0)


class CreateSlaughterTask(TestCase):
    def test__suc(self):
        plan = PlanFactory(quantity=3)
        
        with mock.patch(
            'api.services.model.rabbit.managers._manager.FatteningRabbitManager.status',
            mock.PropertyMock(
                return_value={FatteningRabbit.Manager.STATUS_READY_TO_SLAUGHTER}
            )
        ):
            fattening_rabbits = FatteningRabbitFactory.create_batch(
                2, is_male=True, plan=plan
            )
            SlaughterTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 2)
        for task in Task.objects.select_subclasses():
            self.assertEqual(task.CHAR_TYPE, SlaughterTask.CHAR_TYPE)
            self.assertIn(task.rabbit, fattening_rabbits)
    
    def test__fail(self):
        SlaughterTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 0)
