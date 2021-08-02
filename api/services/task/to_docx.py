from typing import Final, TypedDict, Callable, Type

from docxtpl import DocxTemplate

from api.models import *
from api.serializers.cage.default import OnlyNumberCageSerializer


def _(cage: Cage) -> str:
    repr_ = OnlyNumberCageSerializer().to_representation(cage)
    return f"{repr_['farm_number']}-{repr_['number']}{repr_['letter']}"


class _TypeTaskContext(TypedDict):
    title: str
    description: Callable[[Task], str]


class TypeTaskContext(TypedDict):
    title: str
    description: str


class TaskToDocxService:
    TYPE__CONTEXT: dict[Type[Task], _TypeTaskContext] = {
        ToReproductionTask: {
            'title': 'Отсадка', 'description': lambda t: _(t.cage_to)
        },
        ToFatteningTask: {
            'title': 'Отсадка', 'description': lambda t: _(t.cage_to)
        },
        MatingTask: {
            'title': 'Спаривание',
            'description': lambda t: f"{_(t.mother_rabbit.cage)} -> "
                                     f"{_(t.father_rabbit.cage)}"
        },
        BunnyJiggingTask: {
            'title': 'Отсадка от матери',
            'description': lambda t: f"М: {t.cage_from} -> {t.male_cage_to}, "
                                     f"Ж: {t.cage_from} -> {t.female_cage_to}"
        },
        VaccinationTask: {'title': 'Вакцинация', 'description': lambda t: _(t.cage)},
        SlaughterInspectionTask: {
            'title': 'Осмотр перед убоем', 'description': lambda t: _(t.cage)
        },
        SlaughterTask: {
            'title': 'Убой',
            'description': lambda t: f"{_(t.rabbit.cage)} ({t.rabbit.weight})"
        }
    }
    
    def __init__(self, task):
        self.task: Final = task
    
    @property
    def context(self) -> TypeTaskContext:
        context = self.TYPE__CONTEXT[type(self.task)]
        return {k: v() if callable(v) else v for k, v in context}
