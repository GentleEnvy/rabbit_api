from datetime import datetime, timedelta

from api.models import *
from api.services.filterers.base import BaseFilterer

__all__ = ['RabbitFilterer']


class RabbitFilterer(BaseFilterer):
    model = Rabbit
    
    def filter(
        self, is_male: bool = None, type_: list[str] = None,
        breed: list[int] = None, age_from: int = None, age_to: int = None,
        weight_from: float = None, weight_to: float = None, status: list[str] = None,
        farm_number: list[int] = None, cage_number_from: int = None,
        cage_number_to: int = None
    ):
        queryset = self.queryset
        if is_male is not None:
            queryset = queryset.filter(is_male=is_male)
        if type_:
            queryset = queryset.filter(current_type__in=type_)
        if breed:
            queryset = queryset.filter(breed__in=list(map(int, breed)))
        if age_from is not None:
            queryset = queryset.filter(
                birthday__lte=datetime.utcnow() - timedelta(age_from)
            )
        if age_to is not None:
            queryset = queryset.filter(
                birthday__gte=datetime.utcnow() - timedelta(age_to)
            )
        if weight_from is not None:
            queryset = queryset.filter(weight__gte=weight_from)
        if weight_to is not None:
            queryset = queryset.filter(weight__lte=weight_to)
        
        self.queryset = queryset.filter(
            id__in=[
                rabbit.id for rabbit in queryset
                if
                (
                    status is None or any(s in rabbit.cast.manager.status for s in status)
                ) and (
                    farm_number is None or rabbit.cast.cage.farm_number in farm_number
                ) and (
                    cage_number_from is None or
                    rabbit.cast.cage.number >= cage_number_from
                ) and (
                    cage_number_to is None or rabbit.cast.cage.number <= cage_number_to
                )
            ]
        )
    
    def order_by(self, order):
        queryset = self.queryset
        if order == 'age':
            return queryset.order_by('birthday')
        if order == '-age':
            return queryset.order_by('-birthday')
        if order == 'breed':
            return queryset.order_by('breed__title')
        if order in ('weight', '-weight'):
            return queryset.order_by(order)
        if order == 'sex':
            return list(
                queryset.exclude(is_male=None).order_by('-is_male')
            ) + list(queryset.filter(is_male=None))
        if order == 'farm_number':
            return sorted(queryset, key=lambda r: r.cast.cage.farm_number)
        if order == 'cage_number':
            return sorted(
                queryset, key=lambda r: [r.cast.cage.number, r.cast.cage.letter]
            )
        if order == 'type':
            return sum(
                (
                    list(queryset.filter(current_type=rabbit_class.CHAR_TYPE).all())
                    for rabbit_class in
                    (FatteningRabbit, MotherRabbit, FatherRabbit, Bunny)
                ),
                start=[]
            )
        if order == 'status':
            return sorted(
                queryset,
                key=lambda r: '' if len(status := r.cast.manager.status) == 0 else next(
                    iter(status)
                ), reverse=True
            )
        return queryset
    
    def order_by_plan(self, plan: Plan) -> list:
        selected_rabbits = list(plan.fatteningrabbit_set.all())
        none_weight_rabbits = self.queryset.filter(weight=None)
        queryset = self.queryset.exclude(id__in=[r.id for r in none_weight_rabbits])
        return selected_rabbits + list(none_weight_rabbits) + list(
            queryset.order_by('-weight', 'cage__farm_number')
        )
