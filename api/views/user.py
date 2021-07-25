from django.contrib.auth import get_user_model

from api.serializers.user import UserListSerializer
from api.views.model_views.base import BaseGeneralView

__all__ = ['UserListView']


class UserListView(BaseGeneralView):
    model = get_user_model()
    queryset = get_user_model().objects.order_by('id')
    list_serializer = UserListSerializer
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        if groups := params.get('groups'):
            queryset = queryset.filter(groups__typegroup__type__in=groups.split(','))
        return queryset
