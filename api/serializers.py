from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.utils import model_meta

from api.models import *

__all__ = [
    'RabbitSerializer', 'DeadRabbitSerializer', 'FatteningRabbitSerializer',
    'BunnySerializer', 'MotherRabbitSerializer', 'FatherRabbitSerializer'
]


class RabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = '__all__'


class DeadRabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadRabbit
        fields = '__all__'


class FatteningRabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatteningRabbit
        fields = '__all__'


class BunnySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bunny
        fields = '__all__'


class MotherRabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        model_field_name_dicts = model_meta.get_field_info(self.Meta.model)[1:]
        model_field_names = set()
        for model_field_name_dict in model_field_name_dicts:
            model_field_names |= model_field_name_dict.keys()
        request: Request
        if (request := self.context.get('request')) is not None:
            for param_field, is_access_str in request.query_params.items():
                print(param_field)
                try:
                    is_access = bool(int(is_access_str))
                except ValueError:
                    continue
                if is_access and param_field in model_field_names:
                    field_names.append(param_field)
                elif param_field in field_names:
                    field_names.remove(param_field)
        return field_names


class FatherRabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'
