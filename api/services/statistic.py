from datetime import datetime
from typing import Final

from django.db.models import *

from api.models import *

__all__ = ['StatisticService']


class StatisticService:
    def __init__(self, time_from: datetime, time_to: datetime):
        self.time_from: Final[datetime] = time_from
        self.time_to: Final[datetime] = time_to
    
    def slaughters(self):
        return DeadRabbit.objects.filter(
            death_cause=DeadRabbit.CAUSE_SLAUGHTER, **self._filter('death_day')
        ).count()
    
    def deaths(self):
        return DeadRabbit.objects.exclude(death_cause=DeadRabbit.CAUSE_SLAUGHTER).filter(
            **self._filter('death_day')
        ).count()
    
    def bunny_jigs(self):
        def _last_history(model):
            return model.history.filter(
                history_type='+', id=OuterRef('id'),
                history_date__lt=OuterRef('history_date')
            ).order_by('-history_date').values('id')[:1]
        
        return FatteningRabbit.history.filter(
            history_type='+', **self._filter('history_date')
        ).annotate(
            bunny_created_at=Subquery(_last_history(Bunny)),
            mother_rabbit_created_at=Subquery(_last_history(MotherRabbit)),
            father_rabbit_created_at=Subquery(_last_history(FatherRabbit))
        ).filter(
            Q(bunny_created_at__isnull=False) & (
                (
                    Q(mother_rabbit_created_at__isnull=True) |
                    Q(bunny_created_at__gt=F('mother_rabbit_created_at'))
                ) & (
                    Q(father_rabbit_created_at__isnull=True) |
                    Q(bunny_created_at__gt=F('father_rabbit_created_at'))
                )
            )
        ).count()
    
    def matings(self):
        return Mating.objects.filter(self._filter('time')).count()
    
    def rabbits(self):
        return self.fattenings() + self.mothers() + self.fathers() + self.bunnies()
    
    def fattenings(self):
        return self._population(FatteningRabbit)
    
    def mothers(self):
        return self._population(MotherRabbit)
    
    def fathers(self):
        return self._population(FatherRabbit)
    
    def bunnies(self):
        return self._population(Bunny)
    
    def _population(self, model):
        assert self.time_to == self.time_from
        time = self.time_to
        return model.history.filter(
            history_type='+', history_date__lte=time
        ).annotate(
            death_time=Subquery(
                DeadRabbit.objects.filter(id=OuterRef('id')).values('death_day')
            )
        ).filter(Q(death_time__isnull=True) | Q(death_time__lt=time)).count()
    
    def _filter(self, field: str):
        return {f'{field}__gte': self.time_from, f'{field}__lte': self.time_to}
