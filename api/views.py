from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.generics import CreateAPIView

from api.models import *
from api.serializers import *


def _get_by_id(rabbit_class, rabbit_serializer, request, id):
    rabbit = rabbit_class.objects.get(id=id)
    serializer = rabbit_serializer(rabbit, context={'request': request})
    return Response(serializer.data)


# noinspection PyMethodMayBeStatic
class RabbitView(APIView):
    def get(self, request, id):
        try:
            rabbit = Rabbit.objects.get(id=id)
        except Exception as e:
            return exception_handler(e, {'request', request})
        return redirect(rabbit.get_absolute_url())


# noinspection PyMethodMayBeStatic
class DeadRabbitView(APIView):
    def get(self, request, id):
        return _get_by_id(DeadRabbit, DeadRabbitSerializer, request, id)


# noinspection PyMethodMayBeStatic
class FatteningRabbitView(APIView):
    def get(self, request, id):
        return _get_by_id(FatteningRabbit, FatteningRabbitSerializer, request, id)


# noinspection PyMethodMayBeStatic
class BunnyView(APIView):
    def get(self, request, id):
        return _get_by_id(Bunny, BunnySerializer, request, id)


class BunnyCreateView(CreateAPIView):
    serializer_class = BunnySerializer


# noinspection PyMethodMayBeStatic
class MotherRabbitView(APIView):
    def get(self, request, id):
        return _get_by_id(MotherRabbit, MotherRabbitSerializer, request, id)


class MotherRabbitCreateView(CreateAPIView):
    serializer_class = MotherRabbitSerializer


# noinspection PyMethodMayBeStatic
class FatherRabbitView(APIView):
    def get(self, request, id):
        return _get_by_id(FatherRabbit, FatherRabbitSerializer, request, id)
