# -*- coding: utf-8 -*-
import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader

skip = False
try:
    import consulate
    from simple_settings.dynamic_settings.consul_reader import (
        Reader as ConsulReader
    )
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without consul')
class TestDynamicConsulSettings(object):

    @pytest.fixture
    def settings_dict_to_override_by_consul(self):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {'backend': 'consul'}
            },
            'SIMPLE_STRING': 'simple'
        }

    @pytest.fixture
    def settings_dict_to_override_by_consul_with_prefix(self):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {'backend': 'consul', 'prefix': 'test/'}
            },
            'SIMPLE_STRING': 'simple'
        }

    @pytest.yield_fixture
    def consul(self):
        session = consulate.Consul()

        yield session.kv

        for k in session.kv.keys():
            session.kv.delete(k)

    @pytest.fixture
    def reader(self, settings_dict_to_override_by_consul):
        return get_dynamic_reader(settings_dict_to_override_by_consul)

    @pytest.fixture
    def reader_with_prefix(self, settings_dict_to_override_by_consul_with_prefix):
        return get_dynamic_reader(settings_dict_to_override_by_consul_with_prefix)

    def test_should_return_an_instance_of_consul_reader(
        self, settings_dict_to_override_by_consul
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_consul)
        assert isinstance(reader, ConsulReader)

    def test_should_get_string_in_consul_by_reader(self, consul, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from consul'
        consul.set(key, expected_setting)

        assert reader.get(key) == expected_setting

    def test_should_get_string_in_consul_by_reader_with_prefix(self, consul, reader_with_prefix):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from consul'
        consul.set('test/' + key, expected_setting)

        assert reader_with_prefix.get(key) == expected_setting

    def test_should_set_string_in_consul_by_reader(self, consul, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from redis'
        reader.set(key, expected_setting)

        assert consul.get(key) == expected_setting

    def test_should_set_string_in_consul_by_reader_with_prefix(self, consul, reader_with_prefix):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from redis'
        reader_with_prefix.set(key, expected_setting)

        assert consul.get('test/' + key) == expected_setting

    def test_should_use_consul_reader_with_simple_settings(self, consul):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'consul'}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        consul.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert consul.get('SIMPLE_STRING') == 'foo'

    def test_should_use_consul_reader_with_prefix_with_simple_settings(self, consul):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'consul', 'prefix': 'test/'}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        consul.set('test/SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert consul.get('test/SIMPLE_STRING') == 'foo'

    def test_should_use_consul_reader_with_leadingslash_prefix_with_simple_settings(self, consul):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'consul', 'prefix': '/test/'}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        consul.set('test/SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert consul.get('test/SIMPLE_STRING') == 'foo'


    def test_should_use_consul_reader_with_null_prefix_with_simple_settings(self, consul):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'consul', 'prefix': None}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        consul.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert consul.get('SIMPLE_STRING') == 'foo'
