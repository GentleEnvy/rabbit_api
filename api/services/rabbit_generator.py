from datetime import date, timedelta
import random
from typing import Optional

from api.models import *


class RabbitGenerator:
    @staticmethod
    def get_next_random_rabbit(
        mother: Optional[MotherRabbit], father: Optional[FatherRabbit], cage: Cage
    ) -> Rabbit:
        if MotherCage.objects.filter(pk=cage.id).exists():
            rnd = random.choice(
                [
                    FatherRabbit(
                        is_resting=random.choice([True, False]),
                        is_male=True,
                        is_ill=random.choices(
                            [True, False], weights=[0.05, 0.95], k=1
                        )[0],
                        current_type='P',
                        cage_id=cage.id
                    ),
                    MotherRabbit(
                        status=random.choices(
                            ['F', 'P', ''], weights=[0.4, 0.4, 0.2], k=1
                        )[0],
                        last_childbirth=date.today() - timedelta(
                            days=random.randint(3, 180)
                        ),
                        is_male=False,
                        is_ill=random.choices(
                            [True, False], weights=[0.05, 0.95], k=1
                        )[0],
                        current_type='M',
                        cage_id=cage.id,
                    ),
                ]
            )
        elif FatteningCage.objects.filter(pk=cage.id).exists():
            rnd = random.choice(
                [
                    FatherRabbit(
                        is_resting=random.choice([True, False]),
                        is_male=True,
                        is_ill=random.choices(
                            [True, False], weights=[0.05, 0.95], k=1
                        )[0],
                        current_type='P',
                        cage_id=cage.id
                    ),
                    FatteningRabbit(
                        is_male=random.choice([True, False]),
                        is_ill=random.choices(
                            [True, False], weights=[0.05, 0.95], k=1
                        )[0],
                        current_type='F',
                        cage_id=cage.id,
                    ),
                ]
            )
        else:
            rnd = DeadRabbit(
                death_date=date.today() - timedelta(days=random.randint(1, 150)),
                death_cause=random.choice(['S', 'M', 'I', 'D', 'H', 'C', 'E']),
                is_male=random.choice([True, False]),
                current_type='D'
            )
        rnd.father = father
        rnd.mother = mother
        rnd.birthdate = date.today() - timedelta(days=random.randint(3, 180))
        return rnd
    
    @staticmethod
    def generate_cages(total_cages: int) -> set:
        cage_set = set()
        farm_capacity = total_cages // 3
        for cage_number in range(0, total_cages):
            cage_letter = {0: 'а', 1: 'б', 2: 'в', 3: 'г'}
            cage_set.add(
                random.choices(
                    [
                        MotherCage(
                            # no need in setting pk here when is on production, added for
                            # testing
                            pk=cage_number,
                            is_parallel=random.choice([True, False]),
                            farm_number=cage_number // farm_capacity + 2,
                            number=cage_number // 4,
                            letter=cage_letter.get(cage_number % 4),
                            status=random.choices(
                                ['', 'R', 'C'], weights=[0.8, 0.1, 0.1], k=1
                            )[0]
                        ),
                        FatteningCage(
                            # no need in setting pk here when is on production, added for
                            # testing
                            pk=cage_number,
                            farm_number=cage_number // farm_capacity + 2,
                            number=cage_number // 4,
                            letter=cage_letter.get(cage_number % 4),
                            status=random.choices(
                                ['', 'R', 'C'], weights=[0.8, 0.1, 0.1], k=1
                            )[0]
                        )
                    ], [0.25, 0.75], k=1
                )[0]
            )
        return cage_set
    
    @staticmethod
    def get_random_mom_from_generation(generation_list: list) -> MotherRabbit:
        list_of_moms = []
        for rabbit in generation_list:
            if rabbit.CHAR_TYPE == 'M':
                list_of_moms.append(rabbit)
        return random.choice(list_of_moms) if len(list_of_moms) > 0 else None
    
    @staticmethod
    def get_random_dad_from_generation(generation_list: list) -> FatherRabbit:
        list_of_dads = []
        for rabbit in generation_list:
            if rabbit.CHAR_TYPE == 'P':
                list_of_dads.append(rabbit)
        return random.choice(list_of_dads) if len(list_of_dads) > 0 else None
    
    def random_rabbits_generator(self, generations_amount: int) -> list:
        average_breeding_potential = 4
        total_rabbits = int(
            2 * (1 - average_breeding_potential ** generations_amount) / (
                1 - average_breeding_potential)
        )
        total_cages = total_rabbits // 2 + 1
        cage_set = self.generate_cages(total_cages)
        cages_iterator = iter(cage_set)
        current_generation_list = [
            MotherRabbit(
                status=random.choices(['F', 'P', ''], weights=[0.4, 0.4, 0.2], k=1)[0],
                last_childbirth=date.today() - timedelta(days=random.randint(3, 180)),
                is_male=False,
                current_type='M',
                cage_id=next(iter(cage_set)),
            ),
            FatherRabbit(
                is_resting=random.choice([True, False]),
                is_male=True,
                is_ill=random.choices([True, False], weights=[0.05, 0.95], k=1)[0],
                current_type='P',
                cage_id=next(iter(cage_set)),
            ),
        ]
        next_generation_list = []
        all_generations_list = [*current_generation_list]
        for current_generation in range(generations_amount - 1):
            cage = next(cages_iterator)
            for next_generation in range(
                (current_generation + 1) * average_breeding_potential
            ):
                if len(cage.rabbits) >= 2:
                    cage = next(cages_iterator)
                next_generation_list.append(
                    self.get_next_random_rabbit(
                        self.get_random_mom_from_generation(current_generation_list),
                        self.get_random_dad_from_generation(current_generation_list),
                        cage=cage
                    )
                )
            current_generation_list = next_generation_list.copy()
            all_generations_list += current_generation_list.copy()
            next_generation_list = []
        
        return all_generations_list
