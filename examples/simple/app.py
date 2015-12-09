# -*- coding: utf-8 -*-
import os

from simple_settings import settings


os.environ.setdefault('settings', 'project_settings')
print settings.SIMPLE_CONF
