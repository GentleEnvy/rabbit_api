from parameterized import parameterized
from rest_framework.test import APITestCase

from api.tests.factories import *


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
