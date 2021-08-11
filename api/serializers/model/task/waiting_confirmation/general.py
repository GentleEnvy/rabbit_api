from api.serializers.model.task.anonymous.general import _BaseTaskListSerializer


__all__ = ['WaitingConfirmationTaskListSerializer']


# TODO: base serializer
# noinspection PyMethodMayBeStatic
class WaitingConfirmationTaskListSerializer(_BaseTaskListSerializer):
    class Meta(_BaseTaskListSerializer.Meta):
        fields = _BaseTaskListSerializer.Meta.fields + ['user']
