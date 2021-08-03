import logging

from api.logs.records import CacheMessageLogRecord

logging.setLogRecordFactory(CacheMessageLogRecord)
