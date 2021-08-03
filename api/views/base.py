from django.conf import settings
from django.db.models import Model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.views import set_rollback

from api.exceptions import *

__all__ = ['BaseView']


def _exception_handler(exception):
    try:
        set_rollback()
        try:
            raise exception
        except APIWarning as e:
            api_error = e
        except ClientError as e:
            api_error = e
        except CriticalError as e:
            api_error = e
        except tuple(APIWarning.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = APIWarning.cast_exception(exception_to_cast)
        except tuple(ClientError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = ClientError.cast_exception(exception_to_cast)
        except tuple(CriticalError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = CriticalError.cast_exception(exception_to_cast)
        
        error = api_error
    
    except Exception as e:
        error = CriticalError(str(e))
    
    if settings.DEBUG and isinstance(error, (CriticalError, ClientError)):
        raise exception
    return error.to_response()


# noinspection PyBroadException
class BaseView(GenericAPIView):
    model: Model
    
    @classmethod
    def as_view(cls, **init_kwargs):
        def get_view(view_func):
            def view(*args, **kwargs):
                try:
                    return view_func(*args, **kwargs)
                except Exception as e:
                    return _exception_handler(e)
            
            return view
        
        view_function = super().as_view(**init_kwargs)
        return csrf_exempt(get_view(view_function))
    
    def handle_exception(self, exception):
        return _exception_handler(exception)
