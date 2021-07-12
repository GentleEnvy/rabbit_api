from http import HTTPStatus

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import *
from api.serializers import DeadRabbitRecastSerializer, FatteningRabbitRecastSerializer
from api.views.base import BaseView

__all__ = ['DeadRabbitRecastView', 'FatteningRabbitRecastView']


class _BaseRecastView(BaseView):
    model: Rabbit

    # noinspection PyMethodMayBeStatic
    def post(self, request, id):
        rabbit = Rabbit.objects.get(id=id)
        casted_rabbit = self._recast(rabbit)
        if self.serializer_class is not None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            recast_info = serializer.validated_data
        else:
            recast_info = None
        self._save(casted_rabbit, recast_info)
        return Response(status=HTTPStatus.NO_CONTENT)

    def _recast(self, rabbit):
        return self.model.recast(rabbit)

    @staticmethod
    def _save(casted_rabbit, recast_info=None):
        if recast_info:
            for field_name, field_value in recast_info.items():
                setattr(casted_rabbit, field_name, field_value)
        casted_rabbit.save()


class DeadRabbitRecastView(_BaseRecastView):
    model = DeadRabbit
    serializer_class = DeadRabbitRecastSerializer


class FatteningRabbitRecastView(_BaseRecastView):
    model = FatteningRabbit
    serializer_class = FatteningRabbitRecastSerializer

    def _recast(self, rabbit):
        if rabbit.current_type == FatteningRabbit.CHAR_TYPE:
            raise ValidationError({'current_type': 'Rabbit already fattening'})
        return super()._recast(rabbit)


class ReproductionRabbitRecastView(_BaseRecastView):
    pass
