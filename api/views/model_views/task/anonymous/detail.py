from api.models import Task
from api.serializers import AnonymousTaskUpdateSerializer
from api.views.model_views.base import BaseDetailView

__all__ = ['AnonymousTaskDetailView']


class AnonymousTaskDetailView(BaseDetailView):
    model = Task
    queryset = Task.objects.select_subclasses()
    lookup_url_kwarg = 'id'
    update_serializer = AnonymousTaskUpdateSerializer
