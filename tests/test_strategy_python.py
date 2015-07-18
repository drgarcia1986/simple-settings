# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def python_strategy():
    from simple_settings.strategies import python
    return python.strategy


class TestPythonStrategy(object):

    def test_should_check_a_valid_python_module(self, python_strategy):
        assert python_strategy.is_valid_file(
            'tests.samples.simple'
        ) is True

    def test_should_check_a_invalid_python_module(self, python_strategy):
        assert python_strategy.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_python_module(
        self, python_strategy
    ):
        settings = python_strategy.load_settings_file(
            'tests.samples.simple'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
