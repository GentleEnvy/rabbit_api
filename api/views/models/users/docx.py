from datetime import datetime
import io

from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from docxtpl import DocxTemplate
import pytz

from api.services.model.task import TaskToDocxService
from api.views.base import BaseView

__all__ = ['UserDocxView']


def _create_document(user) -> DocxTemplate:
    return TaskToDocxService(user.task_set.select_subclasses(), user).render()


class UserDocxView(BaseView):
    model = User
    queryset = User.objects.all()
    lookup_url_kwarg = 'id'
    
    _DOCX_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument' \
                         '.wordprocessingml.document'
    
    def get(self, request, **_):
        user = self.get_object()
        buffer = io.BytesIO()
        _create_document(user).save(buffer)
        buffer.seek(0)
        
        response = StreamingHttpResponse(
            streaming_content=buffer,
            content_type=self._DOCX_CONTENT_TYPE
        )
        response['Content-Disposition'] = (
            f'attachment;filename={user.first_name.title()}{user.last_name.title()}_'
            f'{datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%d%m%Y")}.docx'
        )
        response["Content-Encoding"] = 'UTF-8'
        
        return response
