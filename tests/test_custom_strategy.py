# -*- coding: utf-8 -*-
import importlib
import inspect

import pytest

from simple_settings.core import LazySettings


class SettingsLoadStrategyPythonObj(object):
    """
    This is the strategy used to read settings from a python class' attributes.

    this strategy ignores settings that contain lowercase characters.
    """
    name = 'python_obj'


    @staticmethod
    def _load_object(path):
        """Load an object given its absolute object path, and return it.

        object can be a class, function, variable or an instance.
        path ie: 'simple_settings.core.LazySettings'
        """

        try:
            dot = path.rindex('.')
        except ValueError:
            raise ValueError(
                "Error loading object '%s': not a full path" % path)

        module, name = path[:dot], path[dot + 1:]
        mod = importlib.import_module(module)

        try:
            obj = getattr(mod, name)
        except AttributeError:
            raise NameError(
                "Module '%s' doesn't define any object named '%s'" % (
                module, name))

        return obj

    @staticmethod
    def is_valid_file(file_name):
        try:
            obj = SettingsLoadStrategyPythonObj._load_object(file_name)
            return inspect.isclass(obj)
        except (ImportError, TypeError, ValueError, NameError):
            return False

    @staticmethod
    def load_settings_file(settings_file):
        result = {}
        obj = SettingsLoadStrategyPythonObj._load_object(settings_file)
        for k, v in getattr(obj, '__dict__').items():
            if k[0].isupper():
                result[k] = v
        return result


class TestSettingsCustomStrategy(object):

    def test_should_read_class_settings_value(self):
        settings = LazySettings('tests.samples.python_obj.MyConfig')
        settings.add_strategy(SettingsLoadStrategyPythonObj)

        assert settings.START_URLS == ['https://www.google.com']
        assert settings.AUTO_CONNECT == True

    def test_should_not_non_class_settings_value(self):
        settings = LazySettings('tests.samples.python_obj.config_invalid')
        settings.add_strategy(SettingsLoadStrategyPythonObj)

        with pytest.raises(RuntimeError):
            settings.as_dict()

    def test_misconfigured_object_path(self):
        settings = LazySettings('tests.samples.non_existing_module.Config')
        settings.add_strategy(SettingsLoadStrategyPythonObj)

        with pytest.raises(RuntimeError):
            settings.as_dict()

        settings = LazySettings('tests.samples.python_obj.non_existing_class')
        settings.add_strategy(SettingsLoadStrategyPythonObj)

        with pytest.raises(RuntimeError):
            settings.as_dict()
