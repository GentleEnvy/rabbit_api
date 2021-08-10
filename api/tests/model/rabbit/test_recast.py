from datetime import *

from django.test import TestCase
from rest_framework import status as rest_framework_status

from api.models import *
from api.tests.fixtures.init import fixtures as init_fixtures


class TestReproduction(TestCase):
    fixtures = init_fixtures
    
    def test__create_mother_rabbit(self):
        cage = FatteningCage.objects.first()
        self.assertEqual(
            self.client.post(
                '/api/rabbit/reproduction/',
                data={
                    'is_male': True, 'birthday': datetime.utcnow() - timedelta(200),
                    'breed': 1, 'cage': cage.id
                },
                content_type='application/json'
            ).status_code, rest_framework_status.HTTP_201_CREATED
        )
