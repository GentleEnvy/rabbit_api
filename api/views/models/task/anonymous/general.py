from threading import Thread

from api.models import *
from api.serializers import AnonymousTaskListSerializer
from api.services.task.controllers.base import TaskController
from api.services.task.controllers import all_controllers
from api.views.models.task.base import BaseTaskGeneralView

__all__ = ['AnonymousTaskGeneralView']


def _update_tasks():
    for task_controller in all_controllers:
        task_controller().update_anonymous()


class AnonymousTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = AnonymousTaskListSerializer
    # noinspection SpellCheckingInspection
    queryset = TaskController().anonymous.all()
    
    def get(self, request, *args, **kwargs):
        Thread(target=_update_tasks).start()
        return super().get(request, *args, **kwargs)
