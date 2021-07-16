from http import HTTPStatus

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import *
from api.serializers.recast import *
from api.views.base import BaseView

__all__ = [
    'DeadRabbitRecastView', 'FatteningRabbitRecastView', 'ReproductionRabbitRecastView'
]


class _BaseRecastView(BaseView):
    model: Rabbit

    # noinspection PyMethodMayBeStatic
    def post(self, request, id):
        rabbit = Rabbit.objects.get(id=id)
        casted_rabbit = self._recast(rabbit)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recast_info = serializer.validated_data
        for field_name, field_value in recast_info.items():
            setattr(casted_rabbit, field_name, field_value)
        casted_rabbit.save()
        return Response(status=HTTPStatus.NO_CONTENT)

    def _recast(self, rabbit):
        return self.model.recast(rabbit)


class DeadRabbitRecastView(_BaseRecastView):
    model = DeadRabbit
    serializer_class = DeadRabbitRecastSerializer

    def _recast(self, rabbit):
        if rabbit.current_type == FatteningRabbit.CHAR_TYPE:
            raise ValidationError({'current_type': 'Rabbit already dead'})
        return super()._recast(rabbit)


class FatteningRabbitRecastView(_BaseRecastView):
    model = FatteningRabbit
    serializer_class = FatteningRabbitRecastSerializer

    def _recast(self, rabbit):
        if rabbit.current_type == FatteningRabbit.CHAR_TYPE:
            raise ValidationError({'current_type': 'Rabbit already fattening'})
        return super()._recast(rabbit)


class ReproductionRabbitRecastView(BaseView):
    serializer_class = MotherRabbitRecastSerializer

    # noinspection PyMethodMayBeStatic
    def post(self, request, id):
        rabbit = Rabbit.objects.get(id=id)
        if rabbit.current_type in (MotherRabbit.CHAR_TYPE, FatherRabbit.CHAR_TYPE):
            raise ValidationError(
                {'current_type': 'Rabbit already reproduction'}
            )
        is_male = rabbit.is_male
        is_male = request.data.get('is_male') if is_male is None else is_male
        if is_male is None:
            raise ValidationError(
                {'is_male': 'The sex of the reproduction rabbit must be determined'}
            )
        if is_male:
            casted_rabbit = FatherRabbit.recast(rabbit)
            serializer = FatherRabbitRecastSerializer(data=request.data)
        else:
            casted_rabbit = MotherRabbit.recast(rabbit)
            serializer = MotherRabbitRecastSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recast_info = serializer.validated_data
        for field_name, field_value in recast_info.items():
            setattr(casted_rabbit, field_name, field_value)
        casted_rabbit.save()
        return Response(status=HTTPStatus.NO_CONTENT)
