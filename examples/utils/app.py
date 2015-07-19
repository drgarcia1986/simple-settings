# -*- coding: utf-8 -*-
from simple_settings import settings
from simple_settings.utils import settings_stub


# Stub examples
with settings_stub(SOME_SETTING='foo'):
    assert settings.SOME_SETTING == 'foo'
assert settings.SOME_SETTING == 'bar'


@settings_stub(SOME_SETTING='foo')
def get_some_setting():
    return settings.SOME_SETTING

assert get_some_setting() == 'foo'
assert settings.SOME_SETTING == 'bar'
