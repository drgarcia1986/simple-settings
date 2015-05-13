# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    """ Return file content. """

    return open(
        os.path.join(
            os.path.dirname(__file__), fname)
    ).read()


def get_packages(package):
    """ Return root package and all sub-packages. """

    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package,
    that are not in a package themselves.
    """

    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}

setup(
    name='simple-settings',
    version='0.0.0',
    install_requires=[],
    url='https://github.com/drgarcia1986/simple-settings',
    author='Diego Garcia',
    author_email='drgarcia1986@gmail.com',
    keywords='django flask bottle tornado settings configuration conf',
    description='A simple way to manage your project settings',
    long_description=read('README.md'),
    packages=get_packages('simple_settings'),
    packages_data=get_package_data('simple_settings'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
