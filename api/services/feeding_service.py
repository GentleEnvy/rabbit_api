from api.models import *
from datetime import date


class FeedingService:
    FEED_BAG_WEIGHT = 25000
    NORMAL_DAILY_CONSUMPTION = 250
    INCREASED_DAILY_CONSUMPTION = 300

    def __init__(self,
                 feed_bag_weight=FEED_BAG_WEIGHT,
                 normal_daily_consumption=NORMAL_DAILY_CONSUMPTION,
                 increased_daily_consumption=INCREASED_DAILY_CONSUMPTION):
        self.feed_bag_weight = feed_bag_weight
        self.normal_daily_consumption = normal_daily_consumption
        self.increased_daily_consumption = increased_daily_consumption

    @property
    def next_delivery_date(self) -> date:
        feeding_rabbits_amount = len(FatherRabbit.objects.all()) + \
                                 len(MotherRabbit.objects.all()) + \
                                 len(FatteningRabbit.objects.all())
        days_passed = date.today() - FeedBatch.objects.latest('delivery_date').delivery_date
        previous_delivery = FeedBatch.objects.latest('delivery_date').bags_number * self.feed_bag_weight
        feed_left = previous_delivery - (days_passed * feeding_rabbits_amount * self.normal_daily_consumption)
        days_left = feed_left / (feeding_rabbits_amount * self.normal_daily_consumption)
        return date.today() + days_left
