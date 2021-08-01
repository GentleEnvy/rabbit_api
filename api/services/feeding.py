from datetime import date, timedelta
from django.db.models import Sum

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
