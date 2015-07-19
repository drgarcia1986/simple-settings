# -*- coding: utf-8 -*-
import sys

from mock import patch
import pytest


class TestSettingsUtils(object):

    def setup(self):
        with patch.object(
            sys, 'argv', ['', '--settings=tests.samples.simple']
        ):
            from simple_settings import settings
            self.current_settings = settings

        from simple_settings.utils import settings_stub
        self.settings_stub = settings_stub

    def teardown(self):
        self.current_settings = None

    def test_stub_settings_with_context_manager(self):
        with self.settings_stub(SIMPLE_STRING='stubed'):
            assert self.current_settings.SIMPLE_STRING == 'stubed'

        assert self.current_settings.SIMPLE_STRING == 'simple'

    def test_stub_settings_with_decorator(self):
        @self.settings_stub(SIMPLE_STRING='stubed')
        def get_simple_string_from_setting():
            return self.current_settings.SIMPLE_STRING

        assert get_simple_string_from_setting() == 'stubed'
        assert self.current_settings.SIMPLE_STRING == 'simple'

    def test_stub_settings_should_raise_value_error_from_a_wrong_settings(self):  # noqa
        with pytest.raises(ValueError) as exc:
            with self.settings_stub(WRONG_SETTING='ops'):
                pass

        assert 'WRONG_SETTING' in str(exc)
