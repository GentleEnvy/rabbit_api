from datetime import *

import factory
from factory.django import DjangoModelFactory

from api.models import *
from api.tests.factories._user import UserFactory
from api.tests.factories._rabbit import *
from api.tests.factories._cage import *

__all__ = ['ToReproductionTaskFactory', 'MatingTaskFactory']


class ToReproductionTaskFactory(DjangoModelFactory):
    class Meta:
        model = ToReproductionTask
    
    rabbit = factory.SubFactory(FatteningRabbitFactory, is_vaccinated=True)
    user = factory.SubFactory(UserFactory)
    cage_to = factory.LazyAttribute(
        lambda t: FatteningCageFactory() if t.rabbit.is_male else MotherCageFactory()
    )


class MatingTaskFactory(DjangoModelFactory):
    class Meta:
        model = MatingTask
    
    mother_rabbit = factory.SubFactory(
        MotherRabbitFactory, birthday=datetime.utcnow() - timedelta(200)
    )
    father_rabbit = factory.SubFactory(
        FatherRabbitFactory, birthday=datetime.utcnow() - timedelta(200)
    )
    user = factory.SubFactory(UserFactory)
