from api.models import *


def find_optimal_partner(rabbit: Rabbit) -> tuple[Rabbit, int]:
    if not rabbit.is_male and MotherRabbit(rabbit).status == 'P':
        raise ValueError('This rabbit is pregnant, no partner should be found')
    if rabbit.is_ill:
        raise ValueError('This rabbit is ill')
    if rabbit.CHAR_TYPE == 'B':
        raise ValueError('This rabbit is too young to breed')

    # rabbit_breed = rabbit.breed
    is_male = rabbit.is_male
    list_of_rabbits = Rabbit.objects.all()
    d = {rabbit.id: 0}
    used = set()
    for _ in list_of_rabbits:
        min_rabbit = None
        for j in list_of_rabbits:
            if j not in used:
                if min_rabbit is None:
                    min_rabbit = j
                else:
                    d_j = d.get(j.id)
                    d_min = d.get(min_rabbit.id)
                    if d_j is not None and d_min is not None:
                        min_rabbit = j
        if min_rabbit is None or d.get(min_rabbit.id) is None:
            break
        used.add(min_rabbit)
        for parent in (rabbit.mother, rabbit.father, min_rabbit.rabbit_set()):
            if d[min_rabbit.id] + 1 < d[parent.id]:
                d[parent.id] = d[min_rabbit.id] + 1
    max_d = 0
    max_id = rabbit.id
    for partner_id, partner_d in d.items():
        if partner_d > max_d and \
                Rabbit.objects.get(partner_id).is_male != is_male:
            max_d = partner_d
            max_id = partner_id

    if max_id == rabbit.id:
        raise Exception('No suitable rabbits found')

    return Rabbit.objects.get(id=max_id), max_d
