from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

__all__ = ['UserListSerializer']


# noinspection PyMethodMayBeStatic
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'groups', 'first_name', 'last_name']
    
    groups = serializers.SerializerMethodField()
    
    # TODO: manager.type_groups
    def get_groups(self, user):
        # noinspection SpellCheckingInspection
        return [g['type'] for g in user.groups.values(type=F('typegroup__type'))]
