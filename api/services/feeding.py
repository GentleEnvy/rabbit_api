from datetime import date, timedelta

from api.managers import MotherRabbitManager
from api.models import *
from api.models import CommonFeeds, NursingMotherFeeds


class FeedingService:
    FEED_BAG_WEIGHT = 25000
    NORMAL_DAILY_CONSUMPTION = 120
    INCREASED_DAILY_CONSUMPTION = 200
    DAYS_FOR_PROGNOSTICATION = 14
    MILK_AGE_FOR_BUNNY = 14

    def __init__(
            self,
            feed_bag_weight=FEED_BAG_WEIGHT,
            normal_daily_consumption=NORMAL_DAILY_CONSUMPTION,
            increased_daily_consumption=INCREASED_DAILY_CONSUMPTION,
            days_for_prognostication=DAYS_FOR_PROGNOSTICATION,
            milk_age_for_bunny=MILK_AGE_FOR_BUNNY,
    ):
        self.feed_bag_weight = feed_bag_weight
        self.normal_daily_consumption = normal_daily_consumption
        self.increased_daily_consumption = increased_daily_consumption
        self.days_for_plan = days_for_prognostication
        self.milk_age_for_bunny = milk_age_for_bunny

    def next_delivery_date(self) -> (date, date):
        common_feeding = 0
        mother_feeding = 0
        for rabbit in Rabbit.objects.all():
            if (rabbit.cast.manager.age.days >= self.milk_age_for_bunny or
                rabbit.current_type in [
                    Rabbit.TYPE_FATHER,
                    Rabbit.TYPE_FATTENING,
                    Rabbit.TYPE_MOTHER]
                ) and \
                    'FB' not in rabbit.cast.manager.status:
                common_feeding += 1
            if 'FB' in rabbit.cast.manager.status:
                mother_feeding += 1

        common_feed_bags = sum(record.stocks_change for record in CommonFeeds.objects.all())
        mother_feed_bags = sum(record.stocks_change for record in NursingMotherFeeds.objects.all())

        days_left_for_common_feeds = (common_feed_bags * self.feed_bag_weight) / \
                                     (common_feeding * self.normal_daily_consumption)
        days_left_for_mother_feeds = (mother_feed_bags * self.feed_bag_weight) / \
                                     (mother_feeding * self.normal_daily_consumption)

        return (date.today() + timedelta(days_left_for_common_feeds),
                date.today() + timedelta(days_left_for_mother_feeds))

    # TODO: calculate amount of feeding rabbits for each day using prognosis
    def rabbits_with_prognosis(self) -> list:
        rabbits_for_each_day = []
        for day in range(self.days_for_plan):
            td = timedelta(day)
            slaughtered_rabbits = Plan.objects.filter(date=date.today() + td).count()
        return rabbits_for_each_day
