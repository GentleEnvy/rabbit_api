from typing import Final
from datetime import timedelta

from django.forms import model_to_dict
from django.utils.timezone import now

from api.models import *
from api.services.forecast.rabbit._condition import ForecastCondition
from api.services.forecast.rabbit._futures import *

__all__ = ['ForecastRabbitService']


def _get_initial_condition() -> ForecastCondition:
    def __get_rabbits_by_current_type(model_class):
        return set(model_class.objects.filter(current_type=model_class.CHAR_TYPE))

    forecast_condition = ForecastCondition(now().date())
    for bunny in __get_rabbits_by_current_type(Bunny):
        forecast_condition.add_bunny(BunnyFuture(
            status=bunny.manager.status, **model_to_dict(bunny)
        ))
    for fattening_rabbit in __get_rabbits_by_current_type(FatteningRabbit):
        forecast_condition.add_fattening_rabbit(FatteningRabbitFuture(
            status=fattening_rabbit.manager.status, **model_to_dict(fattening_rabbit)
        ))
    for mother_rabbit in __get_rabbits_by_current_type(MotherRabbit):
        if (last_fertilization := mother_rabbit.manager.last_fertilization) is not None:
            last_fertilization = last_fertilization.date()
        forecast_condition.add_mother_rabbit(MotherRabbitFuture(
            status=mother_rabbit.manager.status,
            last_fertilization=last_fertilization,
            last_births=mother_rabbit.manager.last_births,
            **model_to_dict(mother_rabbit)
        ))
    for father_rabbit in __get_rabbits_by_current_type(FatherRabbit):
        forecast_condition.add_father_rabbit(FatherRabbitFuture(
            status=father_rabbit.manager.status, **model_to_dict(father_rabbit)
        ))
    return forecast_condition


class ForecastRabbitService:
    def __init__(self):
        self.initial_condition: Final[ForecastCondition] = _get_initial_condition()

    def predict(self, days: int, every_day: bool = False) -> list[ForecastCondition]:
        conditions = []
        last_condition = None
        current_conditional = self.initial_condition
        for day in range(1, days + 1):
            current_date = self.initial_condition.date + timedelta(day)
            new_conditional = ForecastCondition(current_date)
            for bunny in current_conditional.bunnies:
                bunny.tomorrow_state(new_conditional)
            for fattening_rabbit in current_conditional.fattening_rabbits:
                fattening_rabbit.tomorrow_state(new_conditional)
            for mother_rabbit in current_conditional.mother_rabbits:
                mother_rabbit.tomorrow_state(new_conditional)
            for father_rabbit in current_conditional.father_rabbits:
                father_rabbit.tomorrow_state(new_conditional)
            if every_day:
                conditions.append(new_conditional)
            else:
                last_condition = new_conditional
            current_conditional = new_conditional

        if not every_day:
            conditions.append(last_condition)
        return conditions
