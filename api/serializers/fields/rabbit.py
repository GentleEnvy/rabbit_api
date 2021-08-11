from rest_framework import serializers

from api.logs import warning

__all__ = ['RabbitTypeField']


# noinspection PyAbstractClass
class RabbitTypeField(serializers.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, read_only=True, source='*')
    
    def to_representation(self, rabbit):
        try:
            type_ = self.parent.Meta.model.CHAR_TYPE
            if type_ is not None:
                return type_
        except AttributeError as e:
            warning(
                f'RabbitTypeField could not get self.parent.Meta.model.CHAR_TYPE: {e}'
            )
        return rabbit.cast.CHAR_TYPE
