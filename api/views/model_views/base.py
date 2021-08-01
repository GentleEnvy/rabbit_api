from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import *
from rest_framework import serializers

from api.views.base import *


class _EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []


class BaseGeneralView(ListCreateAPIView, BaseView):
    _EmptySerializer = _EmptySerializer
    
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
    _EmptySerializer = _EmptySerializer
    
    retrieve_serializer: serializers.ModelSerializer = None
    update_serializer: serializers.ModelSerializer = None
    destroy_serializer: serializers.ModelSerializer = None
    
    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'GET':
            if self.retrieve_serializer is not None:
                return self.retrieve_serializer
        elif request.method.upper() in ('PUT', 'PATCH'):
            if self.update_serializer is not None:
                return self.update_serializer
        elif request.method.upper() == 'DELETE':
            if self.destroy_serializer is not None:
                return self.destroy_serializer
        if settings.DEBUG:
            return self._EmptySerializer
        self.http_method_not_allowed(request)
