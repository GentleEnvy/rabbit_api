from api.models import *
from datetime import date


def next_delivery_date() -> date:
    feeding_rabbits_amount = len(FatherRabbit.objects.all()) + \
                             len(MotherRabbit.objects.all()) + \
                             len(FatteningRabbit.objects.all())
    days_passed = date.today() - FeedBatch.objects.latest('delivery_date').delivery_date
    previous_delivery = FeedBatch.objects.latest('delivery_date').bags_number * 25000
    feed_left = previous_delivery - (days_passed * feeding_rabbits_amount * 250)
    days_left = feed_left / (feeding_rabbits_amount * 250)
    if days_left < 7:
        send_warning_running_out_of_stocks()
    return date.today() + days_left


def send_warning_running_out_of_stocks():
    pass
