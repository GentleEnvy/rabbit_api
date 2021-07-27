from datetime import datetime
import re

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from api.models import *


class AvoidInbreedingService:
    DAYS_FOR_SAFE_FERTILIZATION = 3
    TOP_RANGE = 10
    
    def __init__(
        self, days_for_safe_fertilization=DAYS_FOR_SAFE_FERTILIZATION, top_range=TOP_RANGE
    ):
        self.days_for_safe_fertilization = days_for_safe_fertilization
        self.top_range = top_range
    
    def find_optimal_partners(self, rabbit) -> dict:
        self.validate_rabbit(rabbit)
        
        rabbit = rabbit.cast
        
        rabbit_breed = rabbit.breed
        list_of_rabbits = Rabbit.objects.filter(breed=rabbit_breed)
        d = {}
        is_male = rabbit.is_male
        
        for i in list_of_rabbits:
            d[i.id] = float('inf')
        
        d[rabbit.id] = 0
        used = set()
        for _ in list_of_rabbits:
            min_rabbit = None
            for j in list_of_rabbits:
                if j not in used and (min_rabbit is None or d[j.id] < d[min_rabbit.id]):
                    min_rabbit = j
            if d.get(min_rabbit.id) == float('inf'):
                break
            used.add(min_rabbit)
            min_rabbit = min_rabbit.cast
            for relative in (
                min_rabbit.mother, min_rabbit.father, *(
                    {} if min_rabbit.current_type in (
                        Rabbit.TYPE_BUNNY, Rabbit.TYPE_FATTENING
                    ) else min_rabbit.rabbit_set.all()
                )
            ):
                if relative is not None and d[min_rabbit.id] + 1 < d.get(relative.id, -1):
                    d[relative.id] = d[min_rabbit.id] + 1
        
        partners = Rabbit.objects.filter(
            is_male=(not is_male),
            current_type__in=(Rabbit.TYPE_MOTHER, Rabbit.TYPE_FATHER)
        )
        top_partners = {
            k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)
            if len(partners.filter(pk=k))
        }
        # if not len(top_partners):
        #     raise LookupError('No suitable rabbits found')
        
        return top_partners
    
    def find_previous_partners(self, rabbit) -> list:
        self.validate_rabbit(rabbit)
        
        if rabbit.is_male:
            previous_partners = [child.mother.id for child in
                Rabbit.objects.filter(father=rabbit)]
        else:
            previous_partners = [child.father.id for child in
                Rabbit.objects.filter(mother=rabbit)]
        return previous_partners
    
    def validate_rabbit(self, rabbit):
        if rabbit.current_type not in (Rabbit.TYPE_MOTHER, Rabbit.TYPE_FATHER):
            raise ValidationError(
                f'Expected mother or father rabbit, but given '
                f'{re.sub(r"(?<!^)(?=[A-Z])", " ", type(rabbit.cast).__name__).lower()}'
            )
        if rabbit.current_type == Rabbit.TYPE_MOTHER:
            MatingTask.clean_mother_rabbit(rabbit)
            mother_rabbit: MotherRabbit = rabbit.cast
            if mother_rabbit.manager.last_fertilization is not None and (
                mother_rabbit.manager.last_fertilization - datetime.today()
            ).days < self.days_for_safe_fertilization:
                # MAYBE: delete
                raise ValidationError('This rabbit is pregnant, no partner should be found')
        else:  # rabbit is FatherRabbit
            MatingTask.clean_father_rabbit(rabbit)
        if rabbit.warning_status:
            raise ValidationError('This rabbit is ill')
    
    @staticmethod
    def sort_rabbits_by_output_efficiency(rabbits: QuerySet) -> list:
        sorted_rabbits = [
            rabbit for rabbit in sorted(
                rabbits.all(), key=lambda rabbit: rabbit.cast.manager.output_efficiency
            )
        ]
        return sorted_rabbits
