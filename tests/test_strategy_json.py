# -*- coding: utf-8 -*-
import pytest

from simple_settings.strategies.json_file import SettingsLoadStrategyJson


class TestJsonStrategy(object):

    @pytest.fixture
    def strategy_json(self):
        return SettingsLoadStrategyJson

    def test_should_check_a_valid_json_file(self, strategy_json):
        assert strategy_json.is_valid_file('foo.json') is True

    def test_should_check_a_invalid_json_file(self, strategy_json):
        assert strategy_json.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_json_file(self, strategy_json):
        settings = strategy_json.load_settings_file(
            'tests/samples/simple_json_file.json'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
        assert settings['SIMPLE_INT'] == 1
        assert settings['NESTED_JSON'] == {'FOO': 'BAR'}
        assert settings['SIMPLE_LIST'] == [1, 2, 3 ,4]
