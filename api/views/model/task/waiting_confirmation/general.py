from api.models import Task
from api.serializers.model.task.waiting_confirmation.general import *
from api.services.model.task.controllers.base import TaskController
from api.views.model.task.base import BaseTaskGeneralView

__all__ = ['WaitingConfirmationTaskGeneralView']


# TODO: base TaskGeneralView
class WaitingConfirmationTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = WaitingConfirmationTaskListSerializer
    queryset = TaskController().waiting_confirmation.all()
