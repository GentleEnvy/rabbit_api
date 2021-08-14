from threading import Thread

from api.logs import debug
from api.models import *
from api.serializers.model.task.anonymous.general import AnonymousTaskListSerializer
from api.services.model.task.controllers import all_controllers
from api.services.model.task.controllers.base import TaskController
from api.views.model.task.base import BaseTaskGeneralView

__all__ = ['AnonymousTaskGeneralView']


def _update_tasks():
    debug('<< start updating anonymous tasks')
    for task_controller in all_controllers:
        task_controller().update_anonymous()
    debug('anonymous tasks update completed >>')


class AnonymousTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = AnonymousTaskListSerializer
    # noinspection SpellCheckingInspection
    queryset = TaskController().anonymous.all()
    
    def get(self, request, *args, **kwargs):
        Thread(target=_update_tasks).start()
        return super().get(request, *args, **kwargs)
