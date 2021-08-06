from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

__all__ = ['BasePagination']


class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data)
        ]))
