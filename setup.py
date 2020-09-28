from setuptools import setup


def read(fname):
    """ Return file content. """
    with open(fname) as f:
        content = f.read()

    return content


description = 'A simple way to manage your project settings'
try:
    long_description = read('README.rst')
except IOError:
    long_description = description

DYNAMIC_SETTINGS_REQUIRES = ['jsonpickle==1.4.1']
TOML_REQUIRES = ['toml==0.10.1']
YAML_REQUIRES = ['PyYAML==5.3.1']
CONSUL_REQUIRES = ['consulate==0.6.0'] + DYNAMIC_SETTINGS_REQUIRES
DATABASE_REQUIRES = ['SQLAlchemy==1.3.19'] + DYNAMIC_SETTINGS_REQUIRES
MEMCACHED_REQUIRES = ['pymemcache==3.4.0', 'six==1.15.0'] + DYNAMIC_SETTINGS_REQUIRES  # noqa
REDIS_REQUIRES = ['redis==3.5.3', 'six==1.15.0'] + DYNAMIC_SETTINGS_REQUIRES
S3_REQUIRES = ['boto3==1.15.6'] + DYNAMIC_SETTINGS_REQUIRES

ALL_REQUIRES = set(
    CONSUL_REQUIRES +
    DATABASE_REQUIRES +
    MEMCACHED_REQUIRES +
    REDIS_REQUIRES +
    S3_REQUIRES +
    TOML_REQUIRES +
    YAML_REQUIRES
)


download_url = 'https://github.com/drgarcia1986/simple-settings/tarball/master'

setup(
    name='simple-settings',
    version='0.19.1',
    install_requires=[],
    url='https://github.com/drgarcia1986/simple-settings',
    author='Diego Garcia',
    author_email='drgarcia1986@gmail.com',
    keywords='django flask bottle tornado settings configuration conf',
    description=description,
    long_description=long_description,
    download_url=download_url,
    packages=[
        'simple_settings',
        'simple_settings.strategies',
        'simple_settings.dynamic_settings',
    ],
    package_dir={
        'simple_settings': 'simple_settings',
        'strategies': 'simple_settings/strategies',
        'dynamic_settings': 'simple_settings/dynamic_settings',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    extras_require={
        'all': ALL_REQUIRES,
        'consul': CONSUL_REQUIRES,
        'database': DATABASE_REQUIRES,
        'memcached': MEMCACHED_REQUIRES,
        'redis': REDIS_REQUIRES,
        's3': S3_REQUIRES,
        'toml': TOML_REQUIRES,
        'yaml': YAML_REQUIRES,
    }
)
