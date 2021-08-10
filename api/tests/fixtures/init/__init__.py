from api.tests.fixtures.init.cages import fixtures as cages_fixtures
from api.tests.fixtures.init.auth import fixtures as auth_fixtures

__all__ = ['fixtures']

_base_dir = 'init/'
fixtures = cages_fixtures + auth_fixtures + [f'{_base_dir}/breed']
