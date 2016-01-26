# -*- coding: utf-8 -*-
from .cfg import SettingsLoadStrategyCfg
from .python import SettingsLoadStrategyPython


strategies = (
    SettingsLoadStrategyPython(),
    SettingsLoadStrategyCfg()
)
