__all__ = ['web', 'api']

_datefmt = '[%d.%m-%H:%M:%S]'
_class = 'api.logs.formatters.ErrorFormatter'

web = {
    '__name__': 'web_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': 'WEB   | %(asctime)s: %(message)s'
}

api = {
    '__name__': 'api_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': '%(levelname)-7s| %(name)s %(asctime)s <%(module)s->%(funcName)s(%('
              'lineno)d)>: %(message)s'
}
