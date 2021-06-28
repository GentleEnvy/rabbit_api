from django.conf import settings
from django.db.models import Model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.views.exceptions import *

__all__ = ['BaseView']


class BaseView(GenericAPIView):
    model: Model

    def handle_exception(self, exc):
        try:
            try:
                return super().handle_exception(exc)
            except APIError as error:
                return Response(error.serialize())
            except APIException as exception:
                return exception.to_response()
            except APIException.SUPPORT_TO_CAST_EXCEPTIONS as exception_to_cast:
                return APIException.cast_exception(exception_to_cast).to_response()
        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(status=400, data=str(e))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')

        query_params = {
            key: param for key, param in params.items()
            if not key.startswith('__') and not key.endswith('__')
        }
        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)
        filtered_queryset = ordered_queryset.filter(**query_params)
        if limit_from is not None:
            if limit_to is not None:
                return filtered_queryset[int(limit_from):int(limit_to)]
            return filtered_queryset[int(limit_from):]
        if limit_to is not None:
            return filtered_queryset[:int(limit_to)]
        return filtered_queryset
