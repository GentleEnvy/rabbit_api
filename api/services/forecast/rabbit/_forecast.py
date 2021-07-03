from copy import deepcopy
from typing import Final
from datetime import date

from django.forms import model_to_dict
from django.utils.timezone import now

from api.models import *
from api.services.forecast.rabbit._condition import ForecastCondition
from api.services.forecast.rabbit._futures import *


def _get_initial_condition() -> ForecastCondition:
    def __get_rabbits_by_current_type(model_class) -> set[Rabbit]:
        return set(model_class.objects.filter(current_type=model_class.CHAR_TYPE))

    future_sets = []
    for model, future in (
            (Bunny, BunnyFuture),
            (FatteningRabbit, FatteningRabbitFuture),
            (MotherRabbit, MotherRabbitFuture),
            (FatherRabbit, FatteningRabbitFuture)
    ):
        futures = set()
        for rabbit in __get_rabbits_by_current_type(model):
            futures.add(future(
                **model_to_dict(rabbit) | {'status': rabbit.manager.status}
            ))
        future_sets.append(futures)

    return ForecastCondition(now().date(), *future_sets)


class ForecastRabbitService:
    def __init__(self, target_date: date):
        if target_date <= now():
            raise ValueError('The forecast can only be made for the future')
        self.target_date: Final[date] = target_date
        self.initial_condition: Final[ForecastCondition] = _get_initial_condition()
