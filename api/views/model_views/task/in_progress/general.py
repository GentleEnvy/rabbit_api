from api.models import Task
from api.serializers import InProgressTaskListSerializer
from api.services.controllers import *
from api.services.controllers.task.base import TaskController
from api.views.model_views.base import BaseGeneralView

__all__ = ['InProgressTaskGeneralView']


# TODO: base TaskGeneralView
class InProgressTaskGeneralView(BaseGeneralView):
    model = Task
    list_serializer = InProgressTaskListSerializer
    queryset = TaskController().in_progress.select_subclasses()
    
    def get(self, request, *args, **kwargs):
        for task_controller in (
            ToReproductionTaskController, SlaughterTaskController, MatingTaskController,
            BunnyJiggingTaskController, VaccinationTaskController,
            SlaughterInspectionTaskController, FatteningSlaughterTaskController
        ):
            task_controller().update_in_progress()  # MAYBE: update by button
        return super().get(request, *args, **kwargs)
