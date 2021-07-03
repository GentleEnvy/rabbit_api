from api.models import *
from datetime import date, timedelta


def next_delivery_date() -> date:
    feeding_rabbits_amount = len(FatherRabbit.objects.all()) + \
                             len(MotherRabbit.objects.all()) + \
                             len(FatteningRabbit.objects.all())
    days_passed = date.today() - FeedBatch.objects.latest('delivery_date').delivery_date
    previous_delivery = FeedBatch.objects.latest('delivery_date').bags_number * 25000
    feed_left = previous_delivery - (days_passed * feeding_rabbits_amount * 250)
    days_left = feed_left / (feeding_rabbits_amount * 250)
    return days_left
