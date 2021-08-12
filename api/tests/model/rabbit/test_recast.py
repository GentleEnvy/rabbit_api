import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import *

_fp = 'model/rabbit/recast'


@parameterized.parameterized_class(
    'fixtures',
    [
        [[f'{_fp}/init', f'{_fp}/{name}']]
        for name in ('father', 'mother', 'male_fattening', 'female_fattening')
    ]
)
class TestRecastNotWaiting(APITestCase):
    def setUp(self):
        self.rabbit = Rabbit.objects.get().cast
        self.url = f'{self.rabbit.get_absolute_url()}recast/'
    
    def test_recast__suc(self):
        resp = self.client.get(self.url)
        self.assertDictEqual(resp.data, {'waiting_recast': False})
        
        self.client.post(self.url)
        resp = self.client.get(self.url)
        self.assertDictEqual(resp.data, {'waiting_recast': True})
        
        task = Task.objects.select_subclasses().get()
        self.assertEqual(task.rabbit.cast, self.rabbit)
    
    def test_recast__err(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('client_error', resp.data)
