import itertools

from parameterized import parameterized
from rest_framework.test import APITestCase

from api.models import *
from api.tests.factories import *


class RabbitGeneralView(APITestCase):
    def setUp(self):
        m = MotherRabbitFactory()
        p = FatherRabbitFactory()
        BunnyFactory(mother=m, father=p)
        FatteningRabbitFactory(mother=m, father=p)
    
    def test(self):
        resp = self.client.get('/api/rabbit/').data
        self.assertEqual(resp['count'], 4)


class RabbitGeneralView_Plan(APITestCase):
    def setUp(self):
        m = MotherRabbitFactory()
        p = FatherRabbitFactory()
        FatteningRabbitFactory(mother=m, father=p)
        self.plan = PlanFactory()
        with FatteningRabbitFactory.mock_status():
            FatteningRabbitFactory(mother=m, father=p, plan=self.plan)
    
    def test_with_plan(self):
        resp = self.client.get('/api/rabbit/', data={'plan': self.plan.id}).data
        self.assertEqual(resp['count'], 1)
        self.assertEqual(resp['results'][0]['plan'], self.plan.id)
    
    def test_without_plan(self):
        resp = self.client.get('/api/rabbit/', data={'plan': ''}).data
        self.assertEqual(resp['count'], 3)
        self.assertEqual(resp['results'][0].get('plan'), None)


class RabbitGeneralView_IsMale(APITestCase):
    def setUp(self):
        MotherRabbitFactory()
        FatherRabbitFactory()
    
    @parameterized.expand([[1], [0]])
    def test(self, is_male):
        resp = self.client.get('/api/rabbit/', data={'is_male': is_male}).data
        self.assertEqual(resp['count'], 1)
        self.assertEqual(resp['results'][0]['is_male'], is_male)


class RabbitGeneralView_Type(APITestCase):
    def setUp(self):
        m = MotherRabbitFactory()
        p = FatherRabbitFactory()
        BunnyFactory(mother=m, father=p)
        FatteningRabbitFactory(mother=m, father=p)
    
    @parameterized.expand(
        sum(
            map(
                lambda i: list(
                    map(
                        lambda t: [t],
                        itertools.permutations(
                            [
                                MotherRabbit.CHAR_TYPE, FatherRabbit.CHAR_TYPE,
                                FatteningRabbit.CHAR_TYPE, Bunny.CHAR_TYPE
                            ], i
                        )
                    )
                ), range(1, 5)
            ), start=[]
        )
    )
    def test_mother(self, type_):
        resp = self.client.get('/api/rabbit/', data={'type': ','.join(type_)}).data
        self.assertEqual(resp['count'], len(type_))
        self.assertIn(resp['results'][0]['current_type'], type_)
