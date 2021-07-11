from http import HTTPStatus

from rest_framework.response import Response

from api.models import Rabbit, DeadRabbit
from api.serializers import DeadRabbitRecastSerializer
from api.views import BaseView

__all__ = ['DeadRabbitRecastView']


class BaseRecastView(BaseView):
    model: Rabbit

    # noinspection PyMethodMayBeStatic
    def post(self, request, id):
        rabbit = Rabbit.objects.get(id=id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        casted_rabbit = self.model.recast(rabbit)
        self._recast(casted_rabbit, serializer.data)
        return Response(status=HTTPStatus.NO_CONTENT)

    @staticmethod
    def _recast(casted_rabbit, recast_info):
        for field_name, field_value in recast_info.items():
            setattr(casted_rabbit, field_name, field_value)
        casted_rabbit.save()


class DeadRabbitRecastView(BaseRecastView):
    model = DeadRabbit
    serializer_class = DeadRabbitRecastSerializer
