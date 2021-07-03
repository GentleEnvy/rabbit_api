from datetime import datetime, timedelta, date
from typing import Union

from django.utils.timezone import now

__all__ = ['diff_time']


def diff_time(time: Union[date, datetime]) -> timedelta:
    now_time = now()
    return now_time - datetime.combine(time, datetime.min.time(), tzinfo=now_time.tzinfo)
