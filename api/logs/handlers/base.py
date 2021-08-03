from logging import Handler

from api.logs._drainer import LogsDrainer

__all__ = ['BaseHandler']


class BaseHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logs_drainer = LogsDrainer(
            path_to_logs_file='api/logs/logs.log',
            max_line_count=100000,
            directory_to_upload='/rabbit/api/logs'
        )
    
    def handle(self, record):
        self._logs_drainer.check()
        return super().handle(record)
