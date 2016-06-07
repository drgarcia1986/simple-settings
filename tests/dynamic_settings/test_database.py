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
    def sqlite_db(self):
        return 'sqlite:///database_test.db'

    @pytest.fixture
    def settings_dict_to_override_by_database(self, sqlite_db):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {
                    'backend': 'database',
                    'sqlalchemy.url': sqlite_db
                }
            },
            'SIMPLE_STRING': 'simple'
        }

    @pytest.yield_fixture
    def database(self, sqlite_db):
        database = DatabaseOperations(
            {'sqlalchemy.url': sqlite_db}
        )

        yield database

        database.flush()

    @pytest.fixture
    def reader(self, settings_dict_to_override_by_database):
        return get_dynamic_reader(settings_dict_to_override_by_database)

    def test_should_return_an_instance_of_database_reader(
        self, settings_dict_to_override_by_database
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_database)
        assert isinstance(reader, DatabaseReader)

    def test_should_get_string_in_database_by_reader(self, database, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from redis'
        database.set(key, expected_setting)

        assert reader.get(key) == expected_setting

    def test_should_set_string_in_database_by_reader(self, database, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from database'
        reader.set(key, expected_setting)

        assert database.get(key) == expected_setting

    def test_should_use_database_reader_with_simple_settings(
        self, database, sqlite_db
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {
                'backend': 'database',
                'sqlalchemy.url': sqlite_db
            }}
        )

        assert settings.SIMPLE_STRING == 'simple'

        database.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert database.get('SIMPLE_STRING') == 'foo'
