import parameterized
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import *
from api.tests.factories import *


@parameterized.parameterized_class(
    'factory',
    [
        [ToReproductionTaskFactory]
    ]
)
class AnonymousTaskDetailView(APITestCase):
    def setUp(self):
        self.task = self.factory(user=None)
        self.user = UserFactory()
    
    def test__suc(self):
        resp = self.client.put(
            f'/api/task/anonymous/{self.task.id}/', data={'user': self.user.id},
            format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user, Task.objects.get().user)
    
    def test__err_required(self):
        resp = self.client.put(f'/api/task/anonymous/{self.task.id}/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test__err_null(self):
        resp = self.client.put(
            f'/api/task/anonymous/{self.task.id}/', data={'user': None}, format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
