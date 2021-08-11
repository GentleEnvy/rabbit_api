from typing import Final
from datetime import timedelta, datetime

from django.forms import model_to_dict

from api.models import *
from api.services.prediction.rabbit._condition import PredictionCondition
from api.services.prediction.rabbit._futures import *

__all__ = ['PredictionRabbitService']


def _get_initial_condition() -> PredictionCondition:
    predict_condition = PredictionCondition(datetime.utcnow().date())
    for bunny in Bunny.objects.all():
        predict_condition.add_bunny(
            BunnyFuture(status=bunny.manager.status, **model_to_dict(bunny))
        )
    for fattening_rabbit in FatteningRabbit.objects.all():
        predict_condition.add_fattening_rabbit(
            FatteningRabbitFuture(
                status=fattening_rabbit.manager.status, **model_to_dict(fattening_rabbit)
            )
        )
    for mother_rabbit in MotherRabbit.objects.all():
        if (last_fertilization := mother_rabbit.manager.last_fertilization) is not None:
            last_fertilization = last_fertilization.date()
        predict_condition.add_mother_rabbit(
            MotherRabbitFuture(
                status=mother_rabbit.manager.status,
                last_fertilization=last_fertilization,
                last_births=mother_rabbit.manager.last_births,
                **model_to_dict(mother_rabbit)
            )
        )
    for father_rabbit in FatherRabbit.objects.all():
        predict_condition.add_father_rabbit(
            FatherRabbitFuture(
                status=father_rabbit.manager.status, **model_to_dict(father_rabbit)
            )
        )
    return predict_condition


class PredictionRabbitService:
    def __init__(self):
        self.initial_condition: Final[PredictionCondition] = _get_initial_condition()
    
    def predict(self, days: int, every_day: bool = False) -> list[PredictionCondition]:
        conditions = []
        last_condition = None
        current_conditional = self.initial_condition
        for day in range(1, days + 1):
            current_date = self.initial_condition.date + timedelta(day)
            new_conditional = PredictionCondition(current_date)
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
