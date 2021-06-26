from rest_framework import serializers
from rest_framework.utils import model_meta

__all__ = ['BaseModelSerializer']


class BaseModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        if hasattr(self, 'Meta'):
            model_field_name_dicts = model_meta.get_field_info(self.Meta.model)[1:]
            model_field_names = set()
            for model_field_name_dict in model_field_name_dicts:
                model_field_names |= model_field_name_dict.keys()
            if (request := self.context.get('request')) is not None:
                for param_field, is_access_str in request.query_params.items():
                    try:
                        is_access = bool(int(is_access_str))
                    except ValueError:
                        continue
                    if is_access and param_field in model_field_names:
                        field_names.append(param_field)
                    elif param_field in field_names:
                        field_names.remove(param_field)
        return field_names

    def to_representation(self, instance):
        return super().to_representation(instance) | {'pk': instance.pk}

    @property
    def data(self):
        data = super().data
        if 'id' in data:
            data.pop('pk', None)
        return data
