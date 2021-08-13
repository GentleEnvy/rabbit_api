from api.logs.configs.formatters import (
    web,
    api_file as api_file_formatter,
    api_console as api_console_formatter
)

__all__ = ['web_console', 'web_file', 'api_console', 'api_file', 'email_admins']

_level = 'DEBUG'
_file_encoding = 'utf-8'
_file_mode = 'a'
_log_filename = 'api/logs/logs.log'

web_console = {
    '__name__': 'web_console_handler',
    'level': _level,
    'class': 'logging.StreamHandler',
    'formatter': web,
    'stream': 'ext://sys.stdout'
}

web_file = {
    '__name__': 'web_file_handler',
    'level': _level,
    'class': 'api.logs.handlers.FileHandler',
    'formatter': web,
    'filename': _log_filename,
    'mode': _file_mode,
    'encoding': _file_encoding
}

api_console = {
    '__name__': 'api_console_handler',
    'level': _level,
    'class': 'api.logs.handlers.StdHandler',
    'formatter': api_console_formatter
}

api_file = {
    '__name__': 'api_file_handler',
    'level': _level,
    'class': 'api.logs.handlers.FileHandler',
    'formatter': api_file_formatter,
    'filename': _log_filename,
    'mode': _file_mode,
    'encoding': _file_encoding
}

email_admins = {
    '__name__': 'email_admins_handler',
    'level': 'ERROR',
    'class': 'api.logs.handlers.AdminEmailHandler',
    'include_html': True
}
