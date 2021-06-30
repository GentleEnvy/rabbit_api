from api.models import *


def find_optimal_partner(rabbit: Rabbit) -> (Rabbit, int):
    if not rabbit.is_male and MotherRabbit(rabbit).status == 'P':
        raise ValueError('This rabbit is pregnant, no partner should be found')
    if rabbit.is_ill:
        raise ValueError('This rabbit is ill')
    if rabbit.CHAR_TYPE == 'B':
        raise ValueError('This rabbit is too young to breed')

    if rabbit.is_male:
        rabbit = FatherRabbit.objects.get(pk=rabbit.id)
    else:
        rabbit = MotherRabbit.objects.get(pk=rabbit.id)

    # rabbit_breed = rabbit.breed
    list_of_rabbits = Rabbit.objects.all()
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
        min_rabbit = males[min_rabbit.id] if min_rabbit.is_male else females[min_rabbit.id]
        for relative in (min_rabbit.mother,
                         min_rabbit.father,
                         *min_rabbit.rabbit_set.all()):
            if relative is not None and d[min_rabbit.id] + 1 < d[relative.id]:
                d[relative.id] = d[min_rabbit.id] + 1
    max_d = 0
    max_id = rabbit.id
    partners = males if not is_male else females
    # удалить из partners мертвых и маленьких кроликов
    # брать сразу всех максимально отдаленных для нахождения лучшего среди них
    best_breeding_potential = 0
    for partner_id, partner_d in d.items():
        if max_d == float('inf'):
            break
        if partner_d > max_d and partner_id in partners:
            max_d = partner_d
            # max_id = partner_id

    for dist in d.items():
        # and best_breeding_potential < min_rabbit.breeding_potential:
        if dist == max_d:
            pass
            # max_id =

    if max_id == rabbit.id:
        raise Exception('No suitable rabbits found')

    return Rabbit.objects.get(id=max_id), max_d
