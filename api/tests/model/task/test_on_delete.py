from django.test import TestCase


class TestTaskOnDelete(TestCase):
    fixtures = [
        'init/breed',
        
        'init/cages/cage', 'init/cages/mother_cage', 'init/cages/fattening_cage',
        
        'init/auth/group', 'init/auth/type_group', 'init/auth/user',
        
        'model/tasks/on_delete/rabbit', 'model/tasks/on_delete/task'
    ]
