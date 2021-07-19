from datetime import date, timedelta, datetime
import random

from api.models import *

DAYS_FOR_SAFE_FERTILIZATION = 3
TOP_RANGE = 10


def find_optimal_partner(rabbit) -> dict:
    if rabbit.current_type == Rabbit.TYPE_MOTHER:
        mother_rabbit: MotherRabbit = rabbit.cast
        if mother_rabbit.manager.last_fertilization is not None and (
            mother_rabbit.manager.last_fertilization - datetime.today()
        ).days < DAYS_FOR_SAFE_FERTILIZATION:
            raise ValueError('This rabbit is pregnant, no partner should be found')
    if rabbit.warning_status:
        raise ValueError('This rabbit is ill')
    if rabbit.current_type == Rabbit.TYPE_BUNNY:
        raise ValueError('This rabbit is too young to breed')
    
    rabbit = rabbit.cast
    
    rabbit_breed = rabbit.breed
    list_of_rabbits = Rabbit.objects.filter(breed=rabbit_breed)
    d = {}
    males = {m.id: m for m in FatherRabbit.objects.all()}
    females = {f.id: f for f in MotherRabbit.objects.all()}
    is_male = rabbit.is_male
    
    for i in list_of_rabbits:
        d[i.id] = float('inf')
    
    d[rabbit.id] = 0
    used = set()
    for _ in list_of_rabbits:
        min_rabbit = None
        for j in list_of_rabbits:
            if j not in used and (min_rabbit is None or d[j.id] < d[min_rabbit.id]):
                min_rabbit = j
        if d.get(min_rabbit.id) == float('inf'):
            break
        used.add(min_rabbit)
        min_rabbit = min_rabbit.cast
        for relative in (
            min_rabbit.mother, min_rabbit.father, *(
                {} if min_rabbit.current_type in (
                    Rabbit.TYPE_BUNNY, Rabbit.TYPE_FATTENING
                ) else min_rabbit.rabbit_set.all()
            )
        ):
            if relative is not None and d[min_rabbit.id] + 1 < d.get(relative.id, -1):
                d[relative.id] = d[min_rabbit.id] + 1
    partners = Rabbit.objects.filter(
        is_male=(not is_male), current_type__in=(Rabbit.TYPE_MOTHER, Rabbit.TYPE_FATHER)
    )
    top_partners = {
        k: v for k, v in sorted(d.items(), key=lambda item: item[1])
        if len(partners.all().filter(pk=k))
    }
    
    if not len(top_partners):
        raise Exception('No suitable rabbits found')
    
    return top_partners


def get_next_random_rabbit(
    mother: MotherRabbit or None, father: FatherRabbit or None, cage: Cage
) -> Rabbit:
    if MotherCage.objects.filter(pk=cage.id).exists():
        rnd = random.choice(
            [
                FatherRabbit(
                    is_resting=random.choice([True, False]),
                    is_male=True,
                    is_ill=random.choices([True, False], weights=[0.05, 0.95], k=1)[0],
                    current_type='P',
                    cage_id=cage.id
                ),
                MotherRabbit(
                    status=random.choices(
                        ['F', 'P', ''], weights=[0.4, 0.4, 0.2], k=1
                    )[0],
                    last_childbirth=date.today() - timedelta(days=random.randint(3, 180)),
                    is_male=False,
                    is_ill=random.choices([True, False], weights=[0.05, 0.95], k=1)[0],
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
                    is_ill=random.choices([True, False], weights=[0.05, 0.95], k=1)[0],
                    current_type='P',
                    cage_id=cage.id
                ),
                FatteningRabbit(
                    is_male=random.choice([True, False]),
                    is_ill=random.choices([True, False], weights=[0.05, 0.95], k=1)[0],
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


def get_random_mom_from_generation(generation_list: list) -> MotherRabbit:
    list_of_moms = []
    for rabbit in generation_list:
        if rabbit.CHAR_TYPE == 'M':
            list_of_moms.append(rabbit)
    return random.choice(list_of_moms) if len(list_of_moms) > 0 else None


def get_random_dad_from_generation(generation_list: list) -> FatherRabbit:
    list_of_dads = []
    for rabbit in generation_list:
        if rabbit.CHAR_TYPE == 'P':
            list_of_dads.append(rabbit)
    return random.choice(list_of_dads) if len(list_of_dads) > 0 else None


def random_rabbits_generator(generations_amount: int) -> list:
    average_breeding_potential = 4
    total_rabbits = int(
        2 * (1 - average_breeding_potential ** generations_amount) / (
            1 - average_breeding_potential)
    )
    total_cages = total_rabbits // 2 + 1
    cage_set = generate_cages(total_cages)
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
                get_next_random_rabbit(
                    get_random_mom_from_generation(current_generation_list),
                    get_random_dad_from_generation(current_generation_list),
                    cage=cage
                )
            )
        current_generation_list = next_generation_list.copy()
        all_generations_list += current_generation_list.copy()
        next_generation_list = []
    
    return all_generations_list
