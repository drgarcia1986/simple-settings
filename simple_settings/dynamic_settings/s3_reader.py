from .base import BaseReader

try:
    from boto3 import resource
    from botocore.exceptions import ClientError
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "s3" dynamic settings reader\n'
        'you need to install simple-settings with s3 dependency:\n'
        'pip install simple-settings[s3] or pip install boto3'
    )


def _get_or_create_bucket(region, bucket_name):
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

    return s3


class Reader(BaseReader):
    """
    S3 settings Reader
    A simple S3 getter/setter
    """

    _default_conf = {
        'bucket_name': 'simple-settings',
        'region': 'us-east-1'
    }

    def __init__(self, conf):
        super(Reader, self).__init__(conf)

        self.s3 = _get_or_create_bucket(
            region=self.conf['region'],
            bucket_name=self.conf['bucket_name']
        )

    def _get(self, key):
        try:
            response = self.s3.Object(
                self.conf['bucket_name'],
                key
            ).get()
        except ClientError:
            return None

        return response['Body'].read().decode()

    def _set(self, key, value):
        bytes_value = bytes(value, 'utf-8')

        self.s3.Object(
            bucket_name=self.conf['bucket_name'],
            key=key
        ).put(
            Body=bytes_value
        )
