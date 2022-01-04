from api.models import Task
from api.serializers import WaitingConfirmationTaskListSerializer
from api.services.controllers.task.base import TaskController
from api.views.model_views.task.base import BaseTaskGeneralView

__all__ = ['WaitingConfirmationTaskGeneralView']


# TODO: base TaskGeneralView
class WaitingConfirmationTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = WaitingConfirmationTaskListSerializer
    queryset = TaskController().waiting_confirmation.select_subclasses()
