from django.conf import settings
from rest_framework.generics import *
from rest_framework import serializers

from api.serializers.base import EmptySerializer
from api.views.base import *

__all__ = ['BaseGeneralView', 'BaseDetailView']


class BaseGeneralView(ListCreateAPIView, BaseView):
    _EmptySerializer = EmptySerializer
    
    create_serializer: serializers.ModelSerializer = None
    list_serializer: serializers.ModelSerializer = None
    
    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'POST':
            if self.create_serializer is not None:
                return self.create_serializer
        elif request.method.upper() == 'GET':
            if self.list_serializer is not None:
                return self.list_serializer
        if settings.DEBUG:
            return self._EmptySerializer
        self.http_method_not_allowed(request)


class BaseDetailView(RetrieveUpdateAPIView, BaseView):
    _EmptySerializer = EmptySerializer
    
    retrieve_serializer: serializers.ModelSerializer = None
    update_serializer: serializers.ModelSerializer = None
    
    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'GET':
            if self.retrieve_serializer is not None:
                return self.retrieve_serializer
        elif request.method.upper() in ('PUT', 'PATCH'):
            if self.update_serializer is not None:
                return self.update_serializer
        if settings.DEBUG:
            return self._EmptySerializer
        self.http_method_not_allowed(request)
