# -*- coding: utf-8 -*-
import pytest

from simple_settings.strategies.python import SettingsLoadStrategyPython


class TestPythonStrategy(object):

    @pytest.fixture
    def strategy_python(self):
        return SettingsLoadStrategyPython

    def test_should_check_a_valid_python_module(self, strategy_python):
        assert strategy_python.is_valid_file(
            'tests.samples.simple'
        ) is True

    def test_should_check_a_invalid_python_module(self, strategy_python):
        assert strategy_python.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_python_module(
        self, strategy_python
    ):
        settings = strategy_python.load_settings_file(
            'tests.samples.simple'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
