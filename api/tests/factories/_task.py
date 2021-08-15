import factory
from factory.django import DjangoModelFactory

from api.models import *
from api.tests.factories._user import UserFactory
from api.tests.factories._rabbit import FatteningRabbitFactory
from api.tests.factories._cage import *

__all__ = ['ToReproductionTaskFactory']


class ToReproductionTaskFactory(DjangoModelFactory):
    class Meta:
        model = ToReproductionTask
    
    rabbit = factory.SubFactory(FatteningRabbitFactory, is_vaccinated=True)
    user = factory.SubFactory(UserFactory)
    cage_to = factory.LazyAttribute(
        lambda t: FatteningCageFactory() if t.rabbit.is_male else MotherCageFactory()
    )
