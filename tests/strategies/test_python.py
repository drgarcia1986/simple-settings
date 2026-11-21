import logging

import pytest

from simple_settings.strategies.python import SettingsLoadStrategyPython


class TestPythonStrategy:

    @pytest.fixture
    def strategy_python(self):
        return SettingsLoadStrategyPython

    def test_should_check_a_valid_python_module(self, strategy_python):
        assert strategy_python.is_valid_file(
            'tests.samples.simple'
        ) is True

    def test_should_check_a_invalid_python_module(self, strategy_python):
        assert strategy_python.is_valid_file('foo.bar') is False

    @pytest.mark.parametrize('source, error', (
        (
            'import missing_settings_dependency_for_test',
            "ModuleNotFoundError: No module named "
            "'missing_settings_dependency_for_test'",
        ),
        (
            'raise TypeError("settings option requires a string")',
            'TypeError: settings option requires a string',
        ),
    ))
    def test_should_log_python_import_error(
        self, strategy_python, tmp_path, monkeypatch, caplog, source, error
    ):
        (tmp_path / 'broken_settings.py').write_text(source, encoding='utf-8')
        monkeypatch.syspath_prepend(str(tmp_path))

        with caplog.at_level(
            logging.INFO, logger='simple_settings.strategies.python'
        ):
            assert strategy_python.is_valid_file('broken_settings') is False

        message = 'Cannot load broken_settings as python settings file'
        assert message in caplog.text
        assert error in caplog.text

    def test_should_load_dict_with_settings_of_python_module(
        self, strategy_python
    ):
        settings = strategy_python.load_settings_file(
            'tests.samples.simple'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
