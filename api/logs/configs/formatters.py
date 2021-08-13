__all__ = ['web', 'api_console', 'api_file']

_datefmt = '[%d.%m-%H:%M:%S]'
_class = 'api.logs.formatters.ErrorFormatter'

web = {
    '__name__': 'web_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': 'WEB    | %(asctime)s: %(message)s'
}

api_console = {
    '__name__': 'api_console_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': '%(levelname)-7s| <%(module)s->%(funcName)s(%('
              'lineno)d)>: %(message)s'
}

api_file = {
    '__name__': 'api_file_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': '%(levelname)-7s| %(name)s %(asctime)s <%(module)s->%(funcName)s(%('
              'lineno)d)>: %(message)s'
}
