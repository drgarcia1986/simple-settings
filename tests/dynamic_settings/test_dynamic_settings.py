# -*- coding: utf-8 -*-
import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader
from simple_settings.dynamic_settings.base import BaseReader


class Reader(BaseReader):

    def __init__(self, conf):
        super(Reader, self).__init__(conf)
        self._dict = {}

    def _get(self, key):
        return self._dict.get(key)

    def _set(self, key, value):
        self._dict[key] = value


class TestDynamicSettings(object):

    @pytest.fixture
    def settings_dict(self):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {'backend': __name__}
            }
        }

    @pytest.fixture
    def reader(self, settings_dict):
        return get_dynamic_reader(settings_dict)

    def test_should_return_instance_of_fake_dynamic_settings(
        self, settings_dict
    ):
        reader = get_dynamic_reader(settings_dict)
        assert isinstance(reader, Reader)

    def test_should_return_value_of_reader_on_get(self, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple value'
        reader.set(key, expected_setting)

        assert reader.get(key) == expected_setting

    def test_should_override_setting_by_reader_value(self, settings_dict):
        settings = LazySettings('tests.samples.simple')
        settings.configure(**settings_dict)

        assert settings.SIMPLE_STRING == 'simple'

        settings._dynamic_reader.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

    def test_should_update_setting_by_last_reader_value(
        self, settings_dict, reader
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(**settings_dict)

        assert settings.SIMPLE_STRING == 'simple'

        settings._dynamic_reader.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        del settings._dynamic_reader._dict['SIMPLE_STRING']
        assert settings.SIMPLE_STRING == 'dynamic'

    def test_should_use_dynamic_setting_only_for_setting_than_match_pattern(
        self, settings_dict
    ):
        settings = LazySettings('tests.samples.dynamic')

        settings_dict[
            'SIMPLE_SETTINGS'
        ]['DYNAMIC_SETTINGS']['pattern'] = 'SIMPLE_*'

        settings.configure(**settings_dict)

        assert settings.ANOTHER_STRING == 'another'
        settings._dynamic_reader.set('ANOTHER_STRING', 'dynamic')
        assert settings.ANOTHER_STRING == 'another'

        assert settings.SIMPLE_STRING == 'simple'
        settings._dynamic_reader.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

    def test_should_update_settings_in_dynamic_storage(self, settings_dict):
        settings = LazySettings('tests.samples.dynamic')
        settings.configure(**settings_dict)
        settings.setup()

        settings._dynamic_reader.set('SIMPLE_STRING', 'simple')
        settings.configure(SIMPLE_STRING='dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'
        assert settings._dynamic_reader.get('SIMPLE_STRING') == 'dynamic'

    def test_should_update_settings_in_dynamic_storage_only_if_match_pattern(
        self, settings_dict
    ):
        settings = LazySettings('tests.samples.dynamic')

        settings_dict[
            'SIMPLE_SETTINGS'
        ]['DYNAMIC_SETTINGS']['pattern'] = 'SIMPLE_*'

        settings.configure(**settings_dict)
        settings.setup()

        settings._dynamic_reader._set('ANOTHER_STRING', 'another')
        settings.configure(ANOTHER_STRING='dynamic')
        assert settings.ANOTHER_STRING == 'dynamic'
        assert settings._dynamic_reader._get('ANOTHER_STRING') == 'another'

    def test_should_auto_casting_values_in_dynamic_storage(
        self, settings_dict, reader
    ):
        key = 'COMPLEX'
        expected_setting = {'foo': 1, 'bar': ['b1', 2, 'b3'], 'simple': 'yes'}
        reader.auto_casting = True

        reader.set(key, expected_setting)
        assert reader.get(key) == expected_setting

        assert reader._dict['COMPLEX'] != expected_setting
