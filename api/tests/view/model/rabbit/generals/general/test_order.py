from datetime import *
from typing import Callable

import parameterized
from rest_framework.test import APITestCase

from api.models import *
from api.tests.factories import *


def _set_up__age(self):
    self.rabbits = (
        MotherRabbitFactory(birthday=datetime.utcnow() - timedelta(100)),
        MotherRabbitFactory(birthday=datetime.utcnow() - timedelta(50))
    )


def _set_up__breed(self):
    self.rabbits = (
        MotherRabbitFactory(breed=BreedFactory(title='Апорода')),
        MotherRabbitFactory(breed=BreedFactory(title='Бпорода'))
    )


# TODO: weight = None
def _set_up__weight(self):
    self.rabbits = (MotherRabbitFactory(weight=1), MotherRabbitFactory(weight=2.5))


# TODO: sex = None
def _set_up__sex(self):
    m = MotherRabbitFactory()
    p = FatherRabbitFactory()
    # b = BunnyFactory(mother=m, father=p)
    self.rabbits = (p, m)  # , b)


def _set_up__farm_number(self):
    self.rabbits = tuple(
        MotherRabbitFactory(cage=MotherCageFactory(farm_number=i)) for i in range(2, 5)
    )


def _set_up__cage_number(self):
    self.rabbits = (
        MotherRabbitFactory(cage=MotherCageFactory(number=1, letter=MotherCage.LETTER_A)),
        MotherRabbitFactory(cage=MotherCageFactory(number=1, letter=MotherCage.LETTER_B)),
        MotherRabbitFactory(cage=MotherCageFactory(number=2))
    )


def _set_up__type(self):
    m = MotherRabbitFactory()
    p = FatherRabbitFactory()
    b = BunnyFactory(mother=m, father=p)
    f = FatteningRabbitFactory(mother=m, father=p)
    self.rabbits = (f, m, p, b)


@parameterized.parameterized_class(
    [
        {'order': 'age', 'setUp': _set_up__age},
        {'order': 'breed', 'setUp': _set_up__breed},
        {'order': 'weight', 'setUp': _set_up__weight},
        {'order': 'sex', 'setUp': _set_up__sex, 'check_reverse': False},
        {'order': 'farm_number', 'setUp': _set_up__farm_number, 'check_reverse': False},
        {'order': 'cage_number', 'setUp': _set_up__cage_number},
        {'order': 'type', 'setUp': _set_up__type, 'check_reverse': False},
    ]
)
class RabbitGeneralViewOrder(APITestCase):
    order: str
    rabbits: tuple
    check_reverse = True
    
    def test_straight(self):
        resp = self.client.get('/api/rabbit/', data={'__order_by__': self.order}).data
        self.assertEqual(resp['count'], len(self.rabbits))
        for result, rabbit in zip(resp['results'], self.rabbits):
            self.assertEqual(int(result['id']), rabbit.id)
    
    def test_reverse(self):
        if self.check_reverse:
            resp = self.client.get(
                '/api/rabbit/', data={'__order_by__': '-' + self.order}
            ).data
            self.assertEqual(int(resp['count']), len(self.rabbits))
            for result, rabbit in zip(resp['results'], self.rabbits[::-1]):
                self.assertEqual(int(result['id']), rabbit.id)
