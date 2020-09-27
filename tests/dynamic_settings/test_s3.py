import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader

skip = False
try:
    from boto3 import resource
    from botocore.exceptions import ClientError
    from moto import mock_s3

    from simple_settings.dynamic_settings.s3_reader import Reader as S3Reader
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without boto3/moto')
class TestDynamicS3Settings:

    @pytest.fixture
    def region(self):
        return 'sa-east-1'

    @pytest.fixture
    def bucket_name(self):
        return 'ice'

    @pytest.fixture
    def setting_key(self):
        return 'SIMPLE_STRING'

    @pytest.fixture
    def settings_dict_to_override_by_s3(self, region, bucket_name, setting_key):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {
                    'backend': 's3',
                    'bucket_name': bucket_name,
                    'region': region
                }
            },
            setting_key: 'simple'
        }

    @pytest.fixture()
    def mock_s3_resource(self):
        with mock_s3() as ms3:
            yield ms3

    @pytest.fixture
    def reader(self, mock_s3_resource, settings_dict_to_override_by_s3):
        return get_dynamic_reader(settings_dict_to_override_by_s3)

    @pytest.fixture
    def s3(self, mock_s3_resource, region, bucket_name):
        s3 = resource(
            service_name='s3',
            region_name=region
        )

        try:
            s3.meta.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': region
                    }
                )

        yield s3

        for key in s3.Bucket(bucket_name).objects.all():
            key.delete()

        s3.Bucket(bucket_name).delete()

    def _set_value_on_s3(self, s3, bucket_name, key, value):
        bytes_value = bytes(value, 'utf-8')

        s3.Object(
            bucket_name=bucket_name,
            key=key
        ).put(
            Body=bytes_value
        )

    def _get_value_from_s3(self, s3, bucket_name, key):
        response = s3.Object(
            bucket_name,
            key
        ).get()

        if response:
            return response['Body'].read().decode()

    def test_should_return_a_instance_of_s3_reader(
        self, mock_s3_resource, settings_dict_to_override_by_s3
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_s3)
        assert isinstance(reader, S3Reader)

    def test_should_get_string_in_s3_by_reader(
        self, s3, reader, bucket_name, setting_key
    ):
        expected_setting = 'simple from s3'
        self._set_value_on_s3(s3, bucket_name, setting_key, expected_setting)

        assert reader.get(setting_key) == expected_setting

    def test_should_set_string_in_s3_by_reader(
        self, s3, reader, bucket_name, setting_key
    ):
        expected_setting = 'simple from s3'
        reader.set(setting_key, expected_setting)

        assert (
            self._get_value_from_s3(s3, bucket_name, setting_key) ==
            expected_setting
        )

    def test_should_use_s3_reader_with_simple_settings(
        self, bucket_name, region, s3
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 's3',
                    'bucket_name': bucket_name,
                    'region': region
                }
            }
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        self._set_value_on_s3(s3, bucket_name, 'SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert (
            self._get_value_from_s3(s3, bucket_name, 'SIMPLE_STRING') == 'foo'
        )

    def test_should_use_s3_reader_with_prefix_with_simple_settings(
        self, bucket_name, region, s3
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={
                'DYNAMIC_SETTINGS': {
                    'backend': 's3',
                    'bucket_name': bucket_name,
                    'region': region,
                    'prefix': 'MYAPP_'
                }
            }
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        self._set_value_on_s3(
            s3,
            bucket_name,
            'MYAPP_SIMPLE_STRING',
            'dynamic'
        )
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert (
            self._get_value_from_s3(s3, bucket_name, 'MYAPP_SIMPLE_STRING') ==
            'foo'
        )
