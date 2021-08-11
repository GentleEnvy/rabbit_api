from datetime import *

from parameterized import parameterized
from rest_framework import status as rest_framework_status
from rest_framework.test import APITestCase

from api.models import *
from api.tests.fixtures.init import fixtures as init_fixtures


class TestReproduction(APITestCase):
    fixtures = init_fixtures
    
    @parameterized.expand([(True, 1, 382), (False, 3, 292)])
    def test__create_mother_rabbit__suc(self, is_male, breed, cage):
        response = self.client.post(
            '/api/rabbit/reproduction/',
            data={
                'is_male': is_male, 'birthday': datetime.utcnow() - timedelta(200),
                'breed': breed, 'cage': cage
            },
            format='json'
        )
        self.assertEqual(response.status_code, rest_framework_status.HTTP_201_CREATED)
        id = response.data['id']
        response = self.client.get(f"/api/rabbit/{id}/")
        self.assertEqual(response.status_code, rest_framework_status.HTTP_302_FOUND)
        response = self.client.get(response.url)
        self.assertEqual(response.data['is_male'], is_male)
        self.assertEqual(response.data['breed'], Breed.objects.get(id=breed).title)
        cage = Cage.objects.get(id=cage)
        self.assertEqual(response.data['cage']['farm_number'], cage.farm_number)
        self.assertEqual(response.data['cage']['number'], cage.number)
        self.assertEqual(response.data['cage']['letter'], cage.letter)
    
    @parameterized.expand([(True, 1, 292), (False, 3, 382), (False, 100, 9)])
    def test__create_mother_rabbit__err(self, is_male, breed, cage):
        response = self.client.post(
            '/api/rabbit/reproduction/',
            data={
                'is_male': is_male, 'birthday': datetime.utcnow() - timedelta(200),
                'breed': breed, 'cage': cage
            },
            format='json'
        )
        self.assertEqual(response.status_code, rest_framework_status.HTTP_400_BAD_REQUEST)
        self.assertIn('client_error', response.data)
