Python Simple Settings
======================
.. _badges:

.. image:: https://badge.fury.io/py/simple-settings.svg
    :target: https://badge.fury.io/py/simple-settings
    :alt: Package version

.. image:: https://readthedocs.org/projects/simple-settings/badge/?version=latest
    :target: http://simple-settings.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: http://www.quantifiedcode.com/api/v1/project/1b5307f0f1584c3b9c736f976b57e973/badge.svg
    :target: http://www.quantifiedcode.com/app/project/1b5307f0f1584c3b9c736f976b57e973
    :alt: Code Issues

.. image:: https://travis-ci.org/drgarcia1986/simple-settings.svg
    :target: https://travis-ci.org/drgarcia1986/simple-settings
    :alt: Build Status

.. image:: https://coveralls.io/repos/drgarcia1986/simple-settings/badge.svg
    :target: https://coveralls.io/r/drgarcia1986/simple-settings
    :alt: Coverage Status

.. _description:

A simple way to manage your project settings.

It is inspired by Django's settings system but is generic for any python project.
With simple-settings you just need specify your settings module in ``--settings`` arg of command line (or ``SIMPLE_SETTINGS`` of environment) and all settings will be available in ``simple_settings.settings``.

Installation
------------

Use ``pip`` (simple like this project :smile:).

.. code-block:: bash

    $ pip install simple-settings

**simple-settings** is tested with Python 2.7, 3.4, 3.5 and PyPy.

Usage
-----

.. code-block:: bash

    $ python app.py --settings=my_settings


.. code-block:: python

    >>> from simple_settings import settings
    >>> print settings.FOO
    'some value in foo'


Some features
-------------
* Settings by python modules.
* Settings by cfg files.
* Settings by Yaml files.
* Settings inheritance (like a pipeline).
* Special settings.
* Dynamic settings.
* Check more features in `documentation <http://simple-settings.readthedocs.org/en/latest/>`_.

Quick links
-----------
* `Documentation <http://simple-settings.readthedocs.org/en/latest/>`_
* `Examples <https://github.com/drgarcia1986/simple-settings/tree/master/examples>`_
* `Roadmap <https://github.com/drgarcia1986/simple-settings/tree/master/ROADMAP.md>`_
