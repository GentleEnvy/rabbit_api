from api.models import Task
from api.serializers import WaitingConfirmationTaskListSerializer
from api.services.task.controllers.base import TaskController
from api.views.models.task.base import BaseTaskGeneralView

__all__ = ['WaitingConfirmationTaskGeneralView']


# TODO: base TaskGeneralView
class WaitingConfirmationTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = WaitingConfirmationTaskListSerializer
    queryset = TaskController().waiting_confirmation.all()
