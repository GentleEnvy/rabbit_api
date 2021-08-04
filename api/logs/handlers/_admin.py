from django.utils.log import AdminEmailHandler as DjangoAdminEmailHandler

__all__ = ['AdminEmailHandler']


class AdminEmailHandler(DjangoAdminEmailHandler):
    def format_subject(self, subject):
        return subject.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
