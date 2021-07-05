from datetime import datetime, timedelta, date, tzinfo, time
from typing import Union

from django.utils.timezone import utc

__all__ = ['diff_time', 'to_datetime']


def diff_time(
        reduced: Union[date, datetime], deductible: Union[date, datetime],
        tz: tzinfo = utc
) -> timedelta:
    if type(reduced) is date:
        reduced = to_datetime(reduced, tz=tz)
    if type(deductible) is date:
        deductible = to_datetime(deductible, tz=tz)
    return reduced - deductible


def to_datetime(date_: date, time_: time = time(), tz: tzinfo = utc) -> datetime:
    _time = getattr(date_, 'time', lambda: _time)()
    # noinspection SpellCheckingInspection
    tz = getattr(date_, 'tzinfo', lambda: tz)()
    return datetime.combine(date_, time_, tzinfo=tz)
