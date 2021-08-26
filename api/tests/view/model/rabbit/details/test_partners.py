from datetime import *
from unittest import mock

from rest_framework.test import APITestCase

from api.models import *
from api.tests.factories import *


class MotherRabbitPartnersView(APITestCase):
    def test__err_mating(self):
        task: MatingTask = MatingTaskFactory()
        task.mother_rabbit.birthday = datetime.utcnow()
        task.mother_rabbit.save()
        
        resp = self.client.get(
            f'/api/rabbit/mother/{task.mother_rabbit.id}/partners/'
        )
        self.assertIn('warning', resp.data)
        self.assertEqual(['mating'], list(resp.data['warning']['codes']))
    
    def test__err_task(self):
        task: MatingTask = MatingTaskFactory()
        resp = self.client.get(
            f'/api/rabbit/mother/{task.mother_rabbit.id}/partners/'
        )
        self.assertIn('warning', resp.data)
        self.assertIn('mating', resp.data['warning']['codes'])
        self.assertIn('task', resp.data['warning']['codes'])
    
    def test__err_womb(self):
        mother_rabbit = MotherRabbitFactory()
        mother_cage = mother_rabbit.cage
        womb_cage = MotherCageFactory(
            farm_number=mother_cage.farm_number, number=mother_cage.number,
            letter=chr(ord(mother_cage.letter) + 1)
        )
        mother_cage.womb = womb_cage
        mother_cage.save()
        BunnyFactory(cage=womb_cage)
        
        with mock.patch(
            'api.services.model.rabbit.managers._manager.MotherRabbitManager.status',
            mock.PropertyMock(
                return_value={MotherRabbit.Manager.STATUS_READY_FOR_FERTILIZATION}
            )
        ):
            resp = self.client.get(f'/api/rabbit/mother/{mother_rabbit.id}/partners/')
        self.assertIn('warning', resp.data)
        self.assertIn('mating', resp.data['warning']['codes'])
        self.assertIn('womb', resp.data['warning']['codes'])
