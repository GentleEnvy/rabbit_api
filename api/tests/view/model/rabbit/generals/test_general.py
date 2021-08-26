from datetime import *

from parameterized import parameterized
from rest_framework.test import APITestCase

from api.models import *
from api.tests.factories import *
from api.tests.utils.functions import permutations
from api.utils.functions import to_datetime


class RabbitGeneralView(APITestCase):
    def setUp(self):
        m = MotherRabbitFactory()
        p = FatherRabbitFactory()
        BunnyFactory(mother=m, father=p)
        FatteningRabbitFactory(mother=m, father=p)
        FatteningRabbitFactory(
            mother=m, father=p, breed=BreedFactory(title='other_breed')
        )
    
    def test(self):
        resp = self.client.get('/api/rabbit/').data
        self.assertEqual(resp['count'], 5)


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
        permutations(
            [
                MotherRabbit.CHAR_TYPE, FatherRabbit.CHAR_TYPE,
                FatteningRabbit.CHAR_TYPE, Bunny.CHAR_TYPE
            ]
        )
    )
    def test(self, type_):
        resp = self.client.get('/api/rabbit/', data={'type': ','.join(type_)}).data
        self.assertEqual(resp['count'], len(type_))
        for rabbit in resp['results']:
            self.assertIn(rabbit['current_type'], type_)
    
    def test_not_exist(self):
        resp = self.client.get('/api/rabbit/', data={'type': 'not_exist'}).data
        self.assertEqual(resp['count'], 0)


class RabbitGeneralView_Breed(APITestCase):
    def setUp(self):
        MotherRabbitFactory(breed=BreedFactory(id=-1, title='breed_1'))
        MotherRabbitFactory(breed=BreedFactory(id=-2, title='breed_2'))
    
    @parameterized.expand(permutations([-1, -2]))
    def test(self, breed):
        resp = self.client.get(
            '/api/rabbit/', data={'breed': ','.join(map(str, breed))}
        ).data
        self.assertEqual(resp['count'], len(breed))
        for rabbit in resp['results']:
            self.assertIn(
                rabbit['breed'], [b.title for b in Breed.objects.filter(id__in=breed)]
            )
    
    def test_not_exist(self):
        resp = self.client.get('/api/rabbit/', data={'breed': -10 ** 10}).data
        self.assertEqual(resp['count'], 0)


class RabbitGeneralView_Age(APITestCase):
    def setUp(self):
        MotherRabbitFactory(birthday=datetime.utcnow() - timedelta(100))  # 100 days
        MotherRabbitFactory(birthday=datetime.utcnow() - timedelta(50))  # 50 days
    
    @parameterized.expand(
        [
            [49, 101, 2], [None, 101, 2], [49, None, 2],
            [49, 99, 1], [51, 101, 1], [None, 99, 1], [51, None, 1],
            [51, 99, 0], [None, 49, 0], [101, None, 0]
        ]
    )
    def test(self, age_from, age_to, count):
        filters = {} if age_from is None else {'age_from': age_from}
        filters |= {} if age_to is None else {'age_to': age_to}
        resp = self.client.get(
            '/api/rabbit/', data=filters
        ).data
        self.assertEqual(resp['count'], count)
        for rabbit in resp['results']:
            if age_from is not None:
                self.assertGreaterEqual(
                    datetime.utcnow() - timedelta(age_from),
                    to_datetime(rabbit['birthday'])
                )
            if age_to is not None:
                self.assertGreaterEqual(
                    to_datetime(rabbit['birthday']), datetime.utcnow() - timedelta(age_to)
                )
