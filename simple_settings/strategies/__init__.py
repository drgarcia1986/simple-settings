# -*- coding: utf-8 -*-
from . import cfg
from .python import SettingsLoadStrategyPython


strategies = (
    SettingsLoadStrategyPython(),
    cfg.strategy
)
