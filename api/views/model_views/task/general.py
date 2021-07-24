from api.models import *
from api.serializers import TaskListSerializer
from api.services.controllers import *
from api.views.model_views.base import BaseGeneralView

__all__ = ['TaskGeneralView']


class TaskGeneralView(BaseGeneralView):
    model = Task
    list_serializer = TaskListSerializer
    # noinspection SpellCheckingInspection
    queryset = Task.objects.select_subclasses()
    
    def get(self, request, *args, **kwargs):
        for task_controller in (
            ToReproductionTaskController, SlaughterTaskController, MatingTaskController,
            BunnyJiggingTaskController, VaccinationTaskController,
            SlaughterInspectionTaskController, FatteningSlaughterTaskController
        ):
            task_controller().update()
        return super().get(request, *args, **kwargs)
