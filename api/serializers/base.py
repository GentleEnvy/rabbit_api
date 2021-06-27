from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta

__all__ = ['BaseModelSerializer']


class BaseModelSerializer(ModelSerializer):
    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        if hasattr(self, 'Meta'):
            model_fields_dicts = model_meta.get_field_info(self.Meta.model)[1:]
            model_fields = set()
            for model_fields_dict in model_fields_dicts:
                model_fields |= model_fields_dict.keys()
            if (request := self.context.get('request')) is not None:
                query_params = request.query_params
                if (show_fields := query_params.get('__show__')) is not None:
                    for show in show_fields.split(','):
                        if show not in field_names and show in model_fields:
                            field_names.append(show)
                if (not_show_fields := query_params.get('__not_show__')) is not None:
                    for not_show in not_show_fields.split(','):
                        if not_show in field_names:
                            field_names.remove(not_show)
        return field_names
