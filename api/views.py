from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import *
from api.serializers import RabbitSerializer, MotherRabbitSerializer


class RabbitView(APIView):
    def get(self, request, id=None):
        if id is None:
            rabbits = Rabbit.objects.all()
            serializer = RabbitSerializer(rabbits, many=True)
            return Response(serializer.data)
        else:
            rabbit = Rabbit.objects.get(id=id)
            return redirect(reverse('rabbit_url') + )

    def post(self, request: Request):
        print(request.data)
        rabbit = Bunny(**request.data)
        rabbit.full_clean()
        rabbit.save()
        return redirect(reverse('rabbit_url') + str(rabbit.id))


class MotherRabbitView(APIView):
    def get(self, request, id):
        mother_rabbits = MotherRabbit.objects.get(id=id)
        serializer = MotherRabbitSerializer(mother_rabbits, context={'request': request})
        return Response(serializer.data)
