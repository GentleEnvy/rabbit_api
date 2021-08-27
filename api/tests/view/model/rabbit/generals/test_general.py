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


class RabbitGeneralView_Weight(APITestCase):
    def setUp(self):
        MotherRabbitFactory(weight=2)
        MotherRabbitFactory(weight=5)
    
    @parameterized.expand(
        [
            [2, 5, 2], [None, 5, 2], [2, None, 2],
            [2, 3, 1], [3, 5, 1], [None, 2, 1], [5, None, 1],
            [3, 4, 0], [None, 1, 0], [6, None, 0]
        ]
    )
    def test(self, weight_from, weight_to, count):
        filters = {} if weight_from is None else {'weight_from': weight_from}
        filters |= {} if weight_to is None else {'weight_to': weight_to}
        resp = self.client.get(
            '/api/rabbit/', data=filters
        ).data
        self.assertEqual(resp['count'], count)
        for rabbit in resp['results']:
            if weight_from is not None:
                self.assertGreaterEqual(float(rabbit['weight']), weight_from)
            if weight_to is not None:
                self.assertGreaterEqual(weight_to, float(rabbit['weight']))


class RabbitGeneralView_CageNumber(APITestCase):
    def setUp(self):
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=3, number=2))
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=3, number=5))
    
    @parameterized.expand(
        [
            [2, 5, 2], [None, 5, 2], [2, None, 2],
            [2, 3, 1], [3, 5, 1], [None, 2, 1], [5, None, 1],
            [3, 4, 0], [None, 1, 0], [6, None, 0]
        ]
    )
    def test(self, cage_number_from, cage_number_to, count):
        filters = {} if cage_number_from is None else {
            'cage_number_from': cage_number_from
        }
        filters |= {} if cage_number_to is None else {'cage_number_to': cage_number_to}
        resp = self.client.get(
            '/api/rabbit/', data=filters
        ).data
        self.assertEqual(resp['count'], count)
        for rabbit in resp['results']:
            if cage_number_from is not None:
                self.assertGreaterEqual(int(rabbit['cage']['number']), cage_number_from)
            if cage_number_to is not None:
                self.assertGreaterEqual(cage_number_to, int(rabbit['cage']['number']))


class RabbitGeneralView_FarmNumber(APITestCase):
    def setUp(self):
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=2))
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=3))
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=4))
    
    @parameterized.expand(permutations(range(2, 5)))
    def test(self, farm_number):
        resp = self.client.get(
            '/api/rabbit/', data={'farm_number': ','.join(map(str, farm_number))}
        ).data
        self.assertEqual(resp['count'], len(farm_number))
        for rabbit in resp['results']:
            self.assertIn(int(rabbit['cage']['farm_number']), farm_number)
    
    @parameterized.expand(permutations([1, 5]))
    def test_not_exist(self, farm_number):
        resp = self.client.get('/api/rabbit/', data={'farm_number': farm_number}).data
        self.assertEqual(resp['count'], 0)
