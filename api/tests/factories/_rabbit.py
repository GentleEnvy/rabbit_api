from unittest import mock

import factory
from factory.django import DjangoModelFactory

from api.models import *
from api.tests.factories._plan import PlanFactory
from api.tests.factories._breed import BreedFactory
from api.tests.factories._cage import MotherCageFactory, FatteningCageFactory

__all__ = [
    'MotherRabbitFactory', 'FatherRabbitFactory', 'BunnyFactory', 'FatteningRabbitFactory'
]


class MotherRabbitFactory(DjangoModelFactory):
    class Meta:
        model = MotherRabbit
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(MotherCageFactory)
    is_male = False
    is_vaccinated = True


class FatherRabbitFactory(DjangoModelFactory):
    class Meta:
        model = FatherRabbit
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(FatteningCageFactory)
    is_male = True
    is_vaccinated = True


class BunnyFactory(DjangoModelFactory):
    class Meta:
        model = Bunny
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(MotherCageFactory)
    mother = factory.SubFactory(MotherRabbitFactory)
    father = factory.SubFactory(FatherRabbitFactory)


class FatteningRabbitFactory(DjangoModelFactory):
    class Meta:
        model = FatteningRabbit
    
    @classmethod
    def mock_status(cls, status=(FatteningRabbit.Manager.STATUS_READY_TO_SLAUGHTER,)):
        return mock.patch(
            'api.services.model.rabbit.managers._manager.FatteningRabbitManager.status',
            mock.PropertyMock(return_value=set(status))
        )
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(FatteningCageFactory)
    mother = factory.SubFactory(MotherRabbitFactory)
    father = factory.SubFactory(FatherRabbitFactory)
    is_male = True
