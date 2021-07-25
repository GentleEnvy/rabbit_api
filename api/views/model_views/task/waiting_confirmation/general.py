from api.serializers import WaitingConfirmationTaskListSerializer
from api.services.controllers.task.base import TaskController
from api.views.model_views.task.anonymous.general import AnonymousTaskGeneralView

__all__ = ['WaitingConfirmationTaskGeneralView']


# TODO: base TaskGeneralView
class WaitingConfirmationTaskGeneralView(AnonymousTaskGeneralView):
    list_serializer = WaitingConfirmationTaskListSerializer
    queryset = TaskController().waiting_confirmation.select_subclasses()
