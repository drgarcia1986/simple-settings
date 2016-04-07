# -*- coding: utf-8 -*-
import pytest

skip = False
try:
    from simple_settings.strategies.yaml_file import SettingsLoadStrategyYaml
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without PyYaml')
class TestYamlStrategy(object):

    @pytest.fixture
    def strategy_yaml(self):
        return SettingsLoadStrategyYaml

    def test_should_check_a_valid_yaml_file(self, strategy_yaml):
        assert strategy_yaml.is_valid_file('foo.yaml') is True

    def test_should_check_a_valid_yaml_file_yml_extension(self, strategy_yaml):
        assert strategy_yaml.is_valid_file('foo.yml') is True

    def test_should_check_a_invalid_yaml_file(self, strategy_yaml):
        assert strategy_yaml.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_yaml_file(self, strategy_yaml):
        settings = strategy_yaml.load_settings_file(
            'tests/samples/simple_yaml_file.yaml'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
        assert settings['COMPLEX_DICT'] == {'complex': 'dict', 'foo': 'bar'}
        assert settings['COMPLEX_LIST'] == ['foo', 'bar']
