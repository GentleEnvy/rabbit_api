from rest_framework import serializers

__all__ = ['TypedRabbitSerializerMixin']


# noinspection PyMethodMayBeStatic
class TypedRabbitSerializerMixin:
    class Meta:
        fields = ['current_type']
    
    current_type = serializers.SerializerMethodField()
    
    def get_current_type(self, rabbit):
        return rabbit.cast.CHAR_TYPE
