import pytest

from simple_settings.strtobool import strtobool


class TestStrToBool:

    @pytest.mark.parametrize('value', (
        'y', 'Y', 'yes', 't', 'True', 'ON', 1,
    ))
    def test_should_return_true(self, value):
        assert strtobool(value) is True

    @pytest.mark.parametrize('value', (
        'n', 'N', 'no', 'f', 'False', 'OFF', 0,
    ))
    def test_should_return_false(self, value):
        assert strtobool(value) is False

    def test_should_raise_value_error(self):
        with pytest.raises(ValueError):
            strtobool('VERDADEIRO')
