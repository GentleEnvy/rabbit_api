from api.models import *
from api.serializers.task.in_progress import *
from api.services.controllers.task.base import TaskController
from api.services.controllers.task import *
from api.views.model_views.base import BaseDetailView

__all__ = [
    'InProgressTaskDetailView', 'InProgressBunnyJiggingTaskDetailView',
    'InProgressSlaughterInspectionTaskDetailView'
]


class InProgressTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().in_progress.select_subclasses().filter(
        bunnyjiggingtask=None, slaughterinspectiontask=None
    )
    lookup_url_kwarg = 'id'
    update_serializer = InProgressTaskUpdateSerializer


class InProgressBunnyJiggingTaskDetailView(InProgressTaskDetailView):
    model = BunnyJiggingTask
    queryset = BunnyJiggingTaskController().in_progress
    update_serializer = InProgressBunnyJiggingTaskUpdateSerializer


class InProgressSlaughterInspectionTaskDetailView(InProgressTaskDetailView):
    model = SlaughterInspectionTask
    queryset = SlaughterInspectionTaskController().in_progress
    update_serializer = InProgressSlaughterInspectionTaskUpdateSerializer
