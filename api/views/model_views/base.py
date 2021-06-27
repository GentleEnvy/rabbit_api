from rest_framework.generics import *
from rest_framework.serializers import ModelSerializer

from api.views.base import *


class BaseGeneralView(ListCreateAPIView, BaseView):
    create_serializer: ModelSerializer = None
    list_serializer: ModelSerializer = None

    def get_serializer_class(self):
        request = self.request
        if request.method.upper() == 'POST':
            if self.create_serializer is None:
                raise NotImplementedError(f"{self.__class__} doesn't support create")
            return self.create_serializer
        elif request.method.upper() == 'GET':
            if self.list_serializer is None:
                raise NotImplementedError(f"{self.__class__} doesn't support list")
            return self.list_serializer
        self.http_method_not_allowed(request)


class BaseDetailView(RetrieveUpdateDestroyAPIView, BaseView):
    pass
