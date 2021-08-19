from django.test import TestCase
from parameterized import parameterized
from rest_framework.test import APITestCase

from api.models import *
from api.services.inbreeding import AvoidInbreedingService
from api.tests.factories import FatherRabbitFactory, MotherRabbitFactory
from datetime import datetime, timedelta


class TestInbreeding(TestCase):
    # fixtures = ['api/tests/fixtures/services/inbreeding.json']
    
    def setUp(self) -> None:
        b_1 = Breed.objects.create(title='Паннон')
        f_1: FatherRabbit = FatherRabbitFactory(
           id=1, birthday=(datetime.utcnow() - timedelta(days=200))
        )
        m_2: MotherRabbit = MotherRabbitFactory(
            id=2, birthday=(datetime.utcnow() - timedelta(days=200))
        )
        f_3: FatherRabbit = FatherRabbitFactory(
            id=3, birthday=(datetime.utcnow() - timedelta(days=200))
        )
        m_4: MotherRabbit = MotherRabbitFactory(
            id=4, birthday=(datetime.utcnow() - timedelta(days=200))
        )
        f_5: FatherRabbit = FatherRabbitFactory(
            id=5,
            father=f_1,
            mother=m_2,
            birthday=(datetime.utcnow() - timedelta(days=200))
        )
        m_6: MotherRabbit = MotherRabbitFactory(
            id=6, father=f_1, mother=m_2, birthday=(datetime.utcnow() - timedelta(
                days=200))
        )
        f_7 = DeadRabbit.objects.create(
            id=7,
            is_male=True, is_vaccinated=True, weight=4000,
            father=f_3, mother=m_4, breed=b_1, death_cause='S',
            birthday=(datetime.utcnow() - timedelta(days=200))
        )
        f_8: FatherRabbit = FatherRabbitFactory(
            id=8,
            father=f_3,
            mother=m_4,
            birthday=(datetime.utcnow() - timedelta(days=200))
        )
        m_9: MotherRabbit = MotherRabbitFactory(
            id=9,
            father=f_3,
            mother=m_4,
            birthday=(datetime.utcnow() - timedelta(days=200))
        )
        list_to_save = [b_1, f_1, m_2, f_3, m_4, f_5, m_6, f_7, f_8, m_9]
        for element in list_to_save:
            element.save()
    
    @parameterized.expand(((6, 8), (5, 9)))
    def test_inbreeding(self, rabbit_id: int, best_pair: int):
        service = AvoidInbreedingService()
        best_rabbits = service.find_optimal_partners(
            Rabbit.objects.get(pk=rabbit_id)
        )
        best_pair_id = list(best_rabbits.keys())[-1]
        self.assertEqual(best_pair_id, best_pair)
