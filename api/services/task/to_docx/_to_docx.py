from datetime import datetime
from pathlib import Path
from typing import Final, TypedDict, Callable, Type, Union

from django.contrib.auth.models import User
from docxtpl import DocxTemplate

from api.models import *
from api.serializers.cage.default import OnlyNumberCageSerializer


def _get_path_to_template() -> Path:
    return Path(__file__).parent / 'task_template.docx'


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
        },        ToFatteningTask: {
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
    
    def __init__(self, tasks: list, user: User = None, path_to_template: str = None):
        self.tasks: Final[list] = tasks
        self.user: Final[User] = user or tasks[0].user
        self.path_to_template: Final[str] = path_to_template or _get_path_to_template()
    
    @property
    def context(self) -> dict[str, Union[str, list[TypeTaskContext]]]:
        return {
            'tasks': [
                {
                    k: v(task) if callable(v) else v
                    for k, v in self.TYPE__CONTEXT[type(task)].items()
                } for task in self.tasks
            ],
            'date': datetime.utcnow().date().strftime('%d.%m.%Y'),
            'user': f'{self.user.last_name} {self.user.first_name}'
        }
    
    @property
    def template(self) -> DocxTemplate:
        return DocxTemplate(self.path_to_template)
    
    def render(self) -> DocxTemplate:
        document = self.template
        document.render(self.context)
        return document
