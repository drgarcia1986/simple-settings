# -*- coding: utf-8 -*-
import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader

skip = False
try:
    from simple_settings.dynamic_settings.database_reader import (
        Reader as DatabaseReader,
        DatabaseOperations
    )
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without SQLAlchemy')
class TestDynamicDatabaseSettings(object):

    @pytest.fixture
    def settings_dict_to_override_by_database(self):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {'backend': 'database'}
            },
            'SIMPLE_STRING': 'simple'
        }

    @pytest.fixture
    def sqlite_db(self):
        return 'sqlite:///database_test.db'

    @pytest.yield_fixture
    def database(self, sqlite_db):
        database = DatabaseOperations(
            {'sqlalchemy.url': sqlite_db}
        )

        yield database

        database.flush()

    def test_should_return_an_instance_of_database_reader(
        self, settings_dict_to_override_by_database
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_database)
        assert isinstance(reader, DatabaseReader)

    def test_should_return_setting_by_redis_or_by_lazy_settings_obj(
        self, database, sqlite_db
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 'database',
                    'sqlalchemy.url': sqlite_db,
                }
            }
        )

        assert settings.SIMPLE_STRING == 'simple'

        database.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        database.delete('SIMPLE_STRING')
        assert settings.SIMPLE_STRING == 'simple'

    def test_should_use_dynamic_setting_only_for_valid_setttings(
        self, database, sqlite_db
    ):
        settings = LazySettings('tests.samples.dynamic')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 'database',
                    'pattern': 'SIMPLE_*',
                    'sqlalchemy.url': sqlite_db,
                }
            }
        )

        assert settings.ANOTHER_STRING == 'another'
        database.set('ANOTHER_STRING', 'dynamic')
        assert settings.ANOTHER_STRING == 'another'

        assert settings.SIMPLE_STRING == 'simple'
        database.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'
