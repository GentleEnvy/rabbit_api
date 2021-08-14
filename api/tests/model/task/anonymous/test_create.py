from django.test import TestCase
from freezegun import freeze_time

from api.models import *
from api.services.model.task.controllers import BunnyJiggingTaskController

fp = 'model/task/anonymous/create'


class CreateBunnyJiggingTask(TestCase):
    fixtures = ['init/breed', f'{fp}/bunny_jigging']
    
    @freeze_time("2021-02-15")
    def test__suc(self):
        BunnyJiggingTaskController().update_anonymous()
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.CHAR_TYPE, BunnyJiggingTask.CHAR_TYPE)
        self.assertEqual(task.cage_from, MotherCage.objects.get())
    
    @freeze_time("2021-02-14")
    def test__err(self):
        BunnyJiggingTaskController().update_anonymous()
        self.assertEqual(Task.objects.count(), 0)
