from api.models import *
from api.serializers.task.in_progress import *
from api.services.task.controllers.base import TaskController
from api.services.task.controllers import *
from api.views.model_views.base import BaseDetailView

__all__ = [
    'InProgressTaskDetailView', 'InProgressBunnyJiggingTaskDetailView',
    'InProgressSlaughterInspectionTaskDetailView'
]


class InProgressTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().in_progress.filter(
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
