from django.conf import settings
from rest_framework.generics import *
from rest_framework.serializers import ModelSerializer

from api.views.base import *


class BaseGeneralView(ListCreateAPIView, BaseView):
    create_serializer: ModelSerializer = None
    list_serializer: ModelSerializer = None

    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'POST':
            if self.create_serializer is not None:
                return self.create_serializer
        elif request.method.upper() == 'GET':
            if self.list_serializer is not None:
                return self.list_serializer
        self.http_method_not_allowed(request)


class BaseDetailView(RetrieveUpdateAPIView, BaseView):
    retrieve_serializer: ModelSerializer = None
    update_serializer: ModelSerializer = None

    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'GET':
            if self.retrieve_serializer is not None:
                return self.retrieve_serializer
        elif request.method.upper() in ('PUT', 'PATCH'):
            if self.update_serializer is not None:
                return self.update_serializer
        self.http_method_not_allowed(request)
