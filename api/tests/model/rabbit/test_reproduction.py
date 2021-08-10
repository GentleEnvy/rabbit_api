from datetime import *

from rest_framework import status as rest_framework_status
from rest_framework.test import APITestCase

from api.models import *
from api.tests.fixtures.init import fixtures as init_fixtures


class TestReproduction(APITestCase):
    fixtures = init_fixtures
    
    def test__create_mother_rabbit(self):
        cage = FatteningCage.objects.first()
        response = self.client.post(
            '/api/rabbit/reproduction/',
            data={
                'is_male': True, 'birthday': datetime.utcnow() - timedelta(200),
                'breed': 1, 'cage': cage.id
            },
            format='json'
        )
        self.assertEqual(response.status_code, rest_framework_status.HTTP_201_CREATED)
        id = response.data['id']
        response = self.client.get(f"/api/rabbit/{id}/")
        self.assertEqual(response.status_code, rest_framework_status.HTTP_302_FOUND)
        response = self.client.get(response.url)
        print(response.data)
