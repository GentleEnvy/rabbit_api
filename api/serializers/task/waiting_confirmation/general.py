from api.serializers.task.anonymous.general import AnonymousTaskListSerializer

__all__ = ['WaitingConfirmationTaskListSerializer']


# TODO: base serializer
# noinspection PyMethodMayBeStatic
class WaitingConfirmationTaskListSerializer(AnonymousTaskListSerializer):
    class Meta(AnonymousTaskListSerializer.Meta):
        fields = AnonymousTaskListSerializer.Meta.fields + ['user']
