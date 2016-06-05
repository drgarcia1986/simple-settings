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
            'SIMPLE_STRING': 'simple',
            'SIMPLE_BYTES': b'simple'
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

    def test_should_return_an_instance_of_consul_reader(
        self, settings_dict_to_override_by_consul
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_consul)
        assert isinstance(reader, ConsulReader)

    def test_should_override_string_by_consul(self, consul, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from consul'
        consul.set(key, expected_setting)

        assert reader.get(key) == expected_setting

        consul.set(key, expected_setting.encode('utf-8'))
        assert reader.get(key) == expected_setting

    def test_should_return_setting_by_consul_or_by_lazy_settings_obj(
        self, consul
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'consul'}}
        )

        assert settings.SIMPLE_STRING == 'simple'

        consul.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        consul.delete('SIMPLE_STRING')
        assert settings.SIMPLE_STRING == 'simple'

    def test_should_update_setting_in_dynamic_storage_by_lazy_settings_obj(
        self, consul
    ):
        settings = LazySettings('tests.samples.dynamic')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 'consul',
                    'pattern': 'SIMPLE_*',
                }
            }
        )
        settings.setup()

        consul.set('SIMPLE_STRING', 'simple')
        settings.configure(SIMPLE_STRING='dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'
        assert consul.get('SIMPLE_STRING') == 'dynamic'

    def test_should_update_setting_in_dynamic_storage_only_if_match_pattern(
        self, consul
    ):
        settings = LazySettings('tests.samples.dynamic')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 'consul',
                    'pattern': 'SIMPLE_*',
                }
            }
        )
        settings.setup()

        consul.set('ANOTHER_STRING', 'another')
        settings.configure(ANOTHER_STRING='dynamic')
        assert settings.ANOTHER_STRING == 'dynamic'
        assert consul.get('ANOTHER_STRING') == 'another'
