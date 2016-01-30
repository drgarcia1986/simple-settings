# -*- coding: utf-8 -*-
from .cfg import SettingsLoadStrategyCfg
from .python import SettingsLoadStrategyPython
from .yaml_file import SettingsLoadStrategyYaml


strategies = (
    SettingsLoadStrategyPython,
    SettingsLoadStrategyCfg,
    SettingsLoadStrategyYaml
)
