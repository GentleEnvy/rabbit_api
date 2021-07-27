from datetime import date, timedelta

from api.managers import MotherRabbitManager
from api.models import *
from api.models import FeedBatch


class FeedingService:
    FEED_BAG_WEIGHT = 25000
    NORMAL_DAILY_CONSUMPTION = 200
    INCREASED_DAILY_CONSUMPTION = 250
    DAYS_FOR_PROGNOSTICATION = 14
    
    def __init__(
        self,
        feed_bag_weight=FEED_BAG_WEIGHT,
        normal_daily_consumption=NORMAL_DAILY_CONSUMPTION,
        increased_daily_consumption=INCREASED_DAILY_CONSUMPTION,
        days_for_prognostication=DAYS_FOR_PROGNOSTICATION,
    ):
        self.feed_bag_weight = feed_bag_weight
        self.normal_daily_consumption = normal_daily_consumption
        self.increased_daily_consumption = increased_daily_consumption
        self.days_for_plan = days_for_prognostication
    
    def next_delivery_date(self):
        common_rabbits_amount = Rabbit.objects.filter(
            current_type__in=(Rabbit.TYPE_FATHER, Rabbit.TYPE_FATTENING)
        ).count()
        feeding_mothers_amount = 0
        for mother in MotherRabbit.all_current():
            if MotherRabbitManager.STATUS_FEEDS_BUNNY not in mother.manager.status:
                common_rabbits_amount += 1
            else:  # FEEDS_BUNNY not in mother status
                feeding_mothers_amount += 1
        
        last_feed_batch = FeedBatch.objects.last()
        days_left_common = last_feed_batch.common_bags_left * self.feed_bag_weight // (
            common_rabbits_amount * self.normal_daily_consumption
        )
        days_left_mother = last_feed_batch.mother_bags_left * self.feed_bag_weight // (
            feeding_mothers_amount * self.normal_daily_consumption
        )
        return date.today() + timedelta(
            days_left_common if days_left_common < days_left_mother else days_left_mother
        )
    
    # TODO: calculate amount of feeding rabbits for each day using prognosis
    def rabbits_with_prognosis(self) -> list:
        rabbits_for_each_day = []
        for day in range(self.days_for_plan):
            td = timedelta(day)
            slaughtered_rabbits = Plan.objects.filter(date=date.today() + td).count()
        return rabbits_for_each_day
