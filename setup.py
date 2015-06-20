# -*- coding: utf-8 -*-
from setuptools import setup


def read(fname):
    """ Return file content. """
    with open(fname) as f:
        content = f.read()

    return content


description = 'A simple way to manage your project settings'
try:
    long_description = read('README.md')
except IOError:
    long_description = description


setup(
    name='simple-settings',
    version='0.2.0',
    install_requires=[],
    url='https://github.com/drgarcia1986/simple-settings',
    author='Diego Garcia',
    author_email='drgarcia1986@gmail.com',
    keywords='django flask bottle tornado settings configuration conf',
    description=description,
    long_description=long_description,
    download_url='https://github.com/drgarcia1986/simple-settings/tarball/master',
    packages=['simple_settings', 'simple_settings.strategies'],
    package_dir={
        'simple_settings': 'simple_settings',
        'strategies': 'simple_settings/strategies'
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
