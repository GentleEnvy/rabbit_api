from django.conf import settings
from django.db.models import Model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView

from api.exceptions import *

__all__ = ['BaseView']


# noinspection PyBroadException
class BaseView(GenericAPIView):
    model: Model
    
    @classmethod
    def as_view(cls, **init_kwargs):
        def view(*args, **kwargs):
            try:
                return view_function(*args, **kwargs)
            except Exception:
                return CriticalError().to_response()
        
        view_function = super().as_view(**init_kwargs)
        return csrf_exempt(view)
    
    def handle_exception(self, exception):
        try:
            try:
                return super().handle_exception(exception)
            except APIWarning as e:
                api_error = e
            except ClientError as e:
                api_error = e
            except CriticalError as e:
                api_error = e
            except tuple(ClientError.EXCEPTION__CAST.keys()) as exception_to_cast:
                api_error = ClientError.cast_exception(exception_to_cast)
            except tuple(CriticalError.EXCEPTION__CAST.keys()) as exception_to_cast:
                api_error = CriticalError.cast_exception(exception_to_cast)
            
            error = api_error
            
        except Exception as e:
            error = e
        
        if settings.DEBUG and isinstance(error, (CriticalError, ClientError)):
            raise error
        return error.to_response()
