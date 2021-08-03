from datetime import datetime, timedelta, date, time
from typing import Union, TextIO

from dateutil.parser import parse
from django.utils import timezone

__all__ = ['diff_time', 'to_datetime', 'file_line_count']


def diff_time(
    reduced: Union[date, datetime], deductible: Union[date, datetime]
) -> timedelta:
    if type(reduced) is date:
        reduced = to_datetime(reduced)
    if type(deductible) is date:
        deductible = to_datetime(deductible)
    return reduced - deductible


def to_datetime(value: Union[str, date]) -> datetime:
    dt = None
    if isinstance(value, str):
        dt = parse(value)
    elif isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime.combine(value, time())
    if dt is None:
        raise ValueError('value must be date or str')
    return timezone.make_naive(
        dt if timezone.is_aware(dt) else
        dt.replace(tzinfo=timezone.get_current_timezone())
    )


def file_line_count(file: TextIO) -> int:
    """
    :param file: file is opened in 'r' mode
    :return: number of lines in file
    """
    file.seek(0)
    line_count = -1
    for last_line, _ in enumerate(file):
        line_count = last_line
    return line_count + 1
