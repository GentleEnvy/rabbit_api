from datetime import datetime, timedelta, date, tzinfo, time
from typing import Union

from django.utils.timezone import utc

__all__ = ['diff_time']


def diff_time(
        reduced: Union[date, datetime], deductible: Union[date, datetime],
        tz: tzinfo = utc
) -> timedelta:
    if isinstance(reduced, date):
        reduced = date_to_datetime(reduced, tz=tz)
    if isinstance(deductible, date):
        deductible = date_to_datetime(deductible, tz=tz)
    return reduced - deductible


def date_to_datetime(date_: date, time_: time = time(), tz: tzinfo = utc) -> datetime:
    return datetime.combine(date_, time_, tzinfo=tz)
