from datetime import datetime
import re

from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Q

from api.models import *

__all__ = ['AvoidInbreedingService']


class AvoidInbreedingService:
    DAYS_FOR_SAFE_FERTILIZATION = 3
    DAYS_FOR_READY_MATING = 110
    TOP_RANGE = 10
    
    def __init__(
        self,
        days_for_safe_fertilization=DAYS_FOR_SAFE_FERTILIZATION,
        top_range=TOP_RANGE,
        days_for_ready_mating=DAYS_FOR_READY_MATING
    ):
        self.days_for_safe_fertilization = days_for_safe_fertilization
        self.days_for_ready_mating = days_for_ready_mating
        self.top_range = top_range
    
    def find_optimal_partners(self, rabbit) -> dict:
        rabbit = rabbit.cast
        self.validate_rabbit(rabbit)
        
        rabbit_breed = rabbit.breed
        list_of_rabbits = Rabbit.objects.select_subclasses().filter(breed=rabbit_breed)
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
            for relative in (
                min_rabbit.mother, min_rabbit.father, *(
                    [] if isinstance(
                        min_rabbit, (Bunny, FatteningRabbit)
                    ) else min_rabbit.rabbit_set.select_subclasses()
                )
            ):
                if relative is not None and d[min_rabbit.id] + 1 < d.get(relative.id, -1):
                    d[relative.id] = d[min_rabbit.id] + 1
        
        partners = Rabbit.objects.select_subclasses().filter(
            Q(is_male=not is_male) & (~Q(motherrabbit=None) | ~Q(fatherrabbit=None))
        )
        top_partner_ids__kinship: dict[int, int] = {
            k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)
            if len(partners.filter(pk=k))
        }
        validated_top_partner_ids__kinship = {}
        top_partners = Rabbit.objects.select_subclasses().filter(
            id__in=top_partner_ids__kinship
        )
        id__top_partners = {p.id: p for p in top_partners}
        for top_partner_id, top_partner in id__top_partners.items():
            try:
                top_partner.cleaner.for_mating()
                if rabbit.is_male:
                    MatingTask.Cleaner.for_pair(rabbit, top_partner)
                else:
                    MatingTask.Cleaner.for_pair(top_partner, rabbit)
            except ValidationError:
                continue
            validated_top_partner_ids__kinship[top_partner_id] = top_partner_ids__kinship[
                top_partner_id
            ]
        
        return validated_top_partner_ids__kinship
    
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
        if not (isinstance(rabbit, (MotherRabbit, FatherRabbit))):
            raise ValidationError(
                f'Expected mother or father rabbit, but given '
                f'{re.sub(r"(?<!^)(?=[A-Z])", " ", type(rabbit.cast).__name__).lower()}'
            )
        if isinstance(rabbit, MotherRabbit):
            rabbit.cleaner.for_mating()
            if rabbit.manager.last_fertilization is not None and (
                rabbit.manager.last_fertilization - datetime.today()
            ).days < self.days_for_safe_fertilization:
                # MAYBE: delete
                raise ValidationError(
                    'This rabbit is pregnant, no partner should be found'
                )
        else:  # rabbit is FatherRabbit
            rabbit.cast.cleaner.for_mating()
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
