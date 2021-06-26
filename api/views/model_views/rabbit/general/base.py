from api.models import *
from api.views.model_views.base import BaseGeneralView

__all__ = ['BaseRabbitGeneralView']


class BaseRabbitGeneralView(BaseGeneralView):
    model: Rabbit

    def get_queryset(self):
        query_params = {key: param[0] for key, param in self.request.query_params.items()}
        return self.model.objects.filter(**query_params)
