# -*- coding: utf-8 -*-
from simple_settings import LazySettings


settings = LazySettings(
    'first_settings', 'second_settings'
)


print(settings.ONLY_IN_FIRST)
print(settings.ONLY_IN_SECOND)
print(settings.SIMPLE_CONF)
