from rest_framework.mixins import DestroyModelMixin

from api.models import MatingTask
from api.services.model.task.controllers import MatingTaskController
from api.views.base import BaseView

__all__ = ['MatingTaskDetailView']


class MatingTaskDetailView(DestroyModelMixin, BaseView):
    model = MatingTask
    queryset = MatingTaskController().in_progress
    lookup_url_kwarg = 'id'
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
