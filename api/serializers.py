from rest_framework import serializers

from api.models import *


class RabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = '__all__'


class MotherRabbitSerializer(serializers.ModelSerializer):
    rabbit_set = RabbitSerializer(many=True)

    class Meta:
        model = MotherRabbit
        fields = '__all__'
