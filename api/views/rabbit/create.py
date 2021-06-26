from urllib.parse import urlencode

from django.core.exceptions import MultipleObjectsReturned, FieldDoesNotExist
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView

from api.serializers.rabbit.create import *

__all__ = [
    'FatteningRabbitCreateView', 'BunnyCreateView', 'MotherRabbitCreateView',
    'FatherRabbitCreateView'
]


class RedirectCreateView(CreateAPIView):
    def _get_url_by_pk(self, pk):
        model = self.serializer_class.Meta.model
        try:
            return model.objects.get(pk=pk).get_absolute_url()
        except (FieldDoesNotExist, MultipleObjectsReturned, AttributeError):
            return None

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            if pk := response.data.get('pk'):
                if url := self._get_url_by_pk(pk):
                    if query_params := request.query_params:
                        return redirect(f'{url}?{urlencode(query_params)}')
                    return redirect(url)
        return response


class FatteningRabbitCreateView(RedirectCreateView):
    serializer_class = FatteningRabbitCreateSerializer


class BunnyCreateView(CreateAPIView):
    serializer_class = BunnyCreateSerializer


class MotherRabbitCreateView(CreateAPIView):
    serializer_class = MotherRabbitCreateSerializer


class FatherRabbitCreateView(CreateAPIView):
    serializer_class = FatherRabbitCreateSerializer
