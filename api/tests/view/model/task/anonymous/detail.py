import parameterized
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import *
from api.tests.factories import *


# @parameterized.parameterized_class(
#     'factory',
#     [
#         [ToReproductionTaskFactory]
#     ]
# )
class AnonymousTaskDetailView(APITestCase):
    # def test__err_required(self):
    #     print(Task.objects.all())
    #     task = ToReproductionTaskFactory()
    #     task = ToReproductionTaskFactory()
    #     print(Task.objects.all())
    #     resp = self.client.put(f'/api/task/anonymous/{task.id}/')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test__err_null(self):
        task = ToReproductionTaskFactory(user=None)
        user = UserFactory()
        resp = self.client.get('/api/task/anonymous/')
        print(resp.data)
        resp = self.client.patch(
            f'/api/task/anonymous/{task.id}/', data={'user': user.id}, format='json'
        )
        # self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
