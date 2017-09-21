Python Simple Settings
======================
.. _badges:

.. image:: https://badge.fury.io/py/simple-settings.svg
    :target: https://badge.fury.io/py/simple-settings
    :alt: Package version

.. image:: https://api.codacy.com/project/badge/Grade/d5d1a3dece0e48478de9797563b49310
    :target: https://www.codacy.com/app/drgarcia1986/simple-settings?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=drgarcia1986/simple-settings&amp;utm_campaign=Badge_Grade
    :alt: Code Issues

.. image:: https://travis-ci.org/drgarcia1986/simple-settings.svg
    :target: https://travis-ci.org/drgarcia1986/simple-settings
    :alt: Build Status

.. image:: https://coveralls.io/repos/drgarcia1986/simple-settings/badge.svg
    :target: https://coveralls.io/r/drgarcia1986/simple-settings
    :alt: Coverage Status

.. _description:

A simple way to manage your project settings.

**simple-settings** is inspired by Django's settings system but is
generic for any python project.

With simple-settings you just need to specify your settings module using
the ``--settings`` command line arg when invoking your python script (or
``SIMPLE_SETTINGS`` environment var) and all settings will be exposed as
properties of the ``simple_settings.settings`` module.

.. code:: python

    >>> from simple_settings import settings
    >>> print(settings.FOO)
    'some value in foo'

Installation
------------

simple-settings is available on
`Pypi <https://pypi.python.org/pypi/simple-settings>`__.

.. code:: bash

    $ pip install simple-settings

..

    To install simple-settings with all dependencies use ``pip install simple-settings[all]``

**simple-settings** is tested with Python 2.7, 3.4, 3.5 and PyPy.

How this works
--------------

simple-settings reads and stores all variables (or constants if you
prefer) of a python module that you specify. To store your settings you
need at least one setting file (in any of supported formats).

To specify your settings module you have two approaches: with command
line or environment.

For example, imagine that you have a python module for your project
settings and this file is in "*settings/development.py*\ " (a common
example). To load settings of this file you can run your project with
command line arg ``--settings``:

.. code:: bash

    $ python app.py --settings=settings.development

simple-settings accepts ``--simple-settings`` command line arg also.
Or set the environment variable ``SIMPLE_SETTINGS``:

.. code:: bash

    $ export SIMPLE_SETTINGS=settings.development
    $ python app.py

..

    the ``settings`` environment variable is deprecated

The ``simple_settings.settings`` object reads both the command line and
environment in this order (but simple-settings takes the first value it
encounters), to know which file to load.

Another option is use class ``LazySettings`` instead of singleton object
``settings``. With ``LazySettings`` class is possible to determine
settings files in object create:

.. code:: python

    from simple_settings import LazySettings


    settings = LazySettings('settings.development')

If you don't pass any value in *LazySettings* init argument, this class
follow the same behavior of *settings* object.

Example
-------

This is a very dummy example, in real world you would use
simple-settings in more complex cases.

**project\_settings.py**
~~~~~~~~~~~~~~~~~~~~~~~~

In this example we just store a simple string but any python type is
accepted.

.. code:: python

    SIMPLE_CONF = 'simple'

**app.py**
~~~~~~~~~~

You don't need specify which setting *simple-settings* must load, you
can do this with command line or environment.

.. code:: python

    from simple_settings import settings

    print(settings.SIMPLE_CONF)

**Run**
~~~~~~~

You can specify your settings module with command line:

.. code:: bash

    $ python app.py --settings=project_settings
    simple

Or environment:

.. code:: bash

    $ export SIMPLE_SETTINGS=project_settings
    $ python app.py
    simple

Check
`examples <https://github.com/drgarcia1986/simple-settings/tree/master/examples>`__,
in project repository for more usage samples.

as\_dict()
----------

You can check the loaded settings through method ``settings.as_dict()``

.. code:: python

    >>> settings.as_dict()
    {'SIMPLE_CONF': 'simple'}

configure
---------

You can change any settings (and add new settings) in runtime with
method ``configure``:

.. code:: python

    >>> settings.SOME_CONF
    foo
    >>> settings.configure(SOME_CONF='bar')
    >>> settings.SOME_CONF
    bar

..

    If your use ``dynamic settings`` the *configure* method update setting value in dynamic storage too.

Types of settings
-----------------

The simple-settings is prepared to play with the following files types:

-  python modules.
-  cfg files (simple ``key=value`` files).
-  yaml files.
-  json files.
-  toml files.

..

    To simple-settings load settings of yaml files is necessary to install with extra require *yaml*, e.g.: ``pip install simple-settings[yaml]``

..

    For toml files is necessary to install with extras require *toml*, e.g.: ``pip install simple-settings[toml]``

Load multiple settings modules
------------------------------

simple-settings can load more than one setting module without use import
approach, just specify yours settings modules separated by comma. For
example:

.. code:: bash

    $ python app.py --settings=production,amazon,new_relic

simple-setting will load all settings modules in order that was
specified (``production``-> ``amazon`` -> ``new_relic``) overriding
possibles conflicts.

This also works with *LazySettings* class:

.. code:: python

    from simple_settings import LazySettings


    settings = LazySettings('production', 'amazon', 'new_relic')

You can combine any type of settings (*python modules*, *yaml*, etc.).

Ignored settings
----------------

-  Python modules:

   -  Variables starting with ``_``.

-  Cfg files:

   -  Keys starting with ``#``.

Special Settings
----------------

simple-settings has a list of *special settings* that change how
simple-settings will load settings. This *special settings* are specified using
a ``SIMPLE_SETTINGS`` dict in the settings module.

.. code:: python

    SIMPLE_SETTINGS = {
        'OVERRIDE_BY_ENV': True,
        'CONFIGURE_LOGGING': True,
        'REQUIRED_SETTINGS': ('API_TOKEN', 'DB_USER'),
        'DYNAMIC_SETTINGS': {
            'backend': 'redis',
            'pattern': 'DYNAMIC_*',
            'auto_casting': True,
            'prefix': 'MYAPP_'
        }
    }

*Note: special settings may only be specified in python settings files
(not ini, yaml, etc.).*

Configure logging
~~~~~~~~~~~~~~~~~

If you set the *special setting* ``CONFIGURE_LOGGING`` with ``True``,
*simple-settings* will configure the python logging to you. You just need
to define your logging configuration with 
`Python dictConfig format <https://docs.python.org/3.5/library/logging.config.html#configuration-dictionary-schema>`__
and place in ``LOGGING`` setting, e.g.

.. code:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'handlers': {
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'my_log.log',
                'maxBytes': 50 * 1024 * 1024,
                'backupCount': 10,
                'formatter': 'default'
            },
        },
        'loggers': {
            '': {
                'handlers': ['logfile'],
                'level': 'ERROR'
            },
            'my_project': {
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

To use just get logger with ``logging.getLogger()``, e.g.

.. code:: python

    import logging
    logger = logging.getLogger('my_project')


    logger.info('Hello')

..

    Don't forget, *simple-settings* is lazy and it only configures logging after runs ``setup()`` method or after reads some setting.

Override settings value
~~~~~~~~~~~~~~~~~~~~~~~

You can override the values of your settings module with environment
variables. You just need set the *special setting* ``OVERRIDE_BY_ENV``
with ``True`` as value.

.. code:: bash

    $ export SIMPLE_CONF="simple from env"
    $ python app.py --settings=project_settings
    simple from env

..

    This is not a dynamic behavior, because settings is only override in *"settings setup"* time, see ``dynamic settings`` for a real dynamic behavior.

Required Settings
~~~~~~~~~~~~~~~~~

You can determine a list of mandatory settings, i.e. settings that
require a valid value. For this, set the *sepecial setting*
``REQUIRED_SETTINGS`` with a list (or any iterable) of yours required
settings. If any setting of this list have an invalid value (or is not
present in setting file) a ``ValueError`` is raised with a list of
required settings not satify in settings file.

Dynamic Settings
~~~~~~~~~~~~~~~~

simple-settings has a list of *dynamic settings* mechanisms that change
a value of setting dynamically. If dynamic setting is activate, for all
setting the dynamic reader is called. The current dynamic mechanisms
suported is:

Default Dynamic Settings Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For all *dynamic settings* backends *simple-settings* accept this
optional parameters:

-  ``pattern``: if you set some regex pattern the dynamic settings
   reader only get settings that match with this pattern. (Note that the
   pattern will be applied to key as entered, ignoring any configured
   ``prefix`` setting.)
-  ``auto_casting``: if you set this conf to ``True`` (default is
   ``False``) *simple settings* use
   `jsonpickle <https://github.com/jsonpickle/jsonpickle>`__ to encode
   settings value before save in dynamic storage and decode after read
   from dynamic storage. With this bahavior you can use complex types
   (like *dict* and *list*) in dynamic settings.
-  ``prefix``: if you set a prefix this value will be prepended to the
   keys when looked up on the backend. The value is prepended without
   any interpretation, so the key
   ``key="MYKEY" and prefix="my/namespace/"`` would resolve to
   ``key="my/namespace/MYKEY"`` and
   ``key="MYKEY" and prefix="MY_NAMESPACE_"`` would resolve to
   ``key="MY_NAMESPACE_MYKEY"``.

Redis
^^^^^

You can read your settings dynamically in redis if you activate the
``DYNAMIC_SETTINGS`` special setting with ``redis`` backend:

.. code:: python

    SIMPLE_SETTINGS = {
        'DYNAMIC_SETTINGS': {
            'backend': 'redis',
            'host': 'locahost',
            'port': 6379,
        }
    }

..

    for ``redis`` backend ``localhost`` is default value for ``host`` and ``6379`` is the default value for ``port``.

In redis dynamic reader the binary types is automatically decoded.

    To install with redis dependencies use:
    ``pip install simple-settings[redis]``

Consul
^^^^^^

You can read your settings dynamically from a consul server if you
activate the ``DYNAMIC_SETTINGS`` special setting with the ``consul``
backend (uses `consulate <https://github.com/gmr/consulate>`__ library):

.. code:: python

    SIMPLE_SETTINGS = {
        'DYNAMIC_SETTINGS': {
            'backend': 'consul',
            'host': 'locahost',
            'port': 8500,
            'prefix': 'mynamespace/'
        }
    }

..

    for ``consul`` backend ``localhost`` is default value for ``host`` and ``8500`` is the default value for ``port``.

Additional attributes for consul backend: ``datacenter``, ``token``,
``scheme``.

    To install with consul dependencies use:
    ``pip install simple-settings[consul]``

DATABASE
^^^^^^^^

You can read your settings dynamically form a database if you activate
the ``DYNAMIC_SETTINGS`` special setting with the ``database`` backend
(uses `sqlalchey <http://docs.sqlalchemy.org/>`__ library)

.. code:: python

    SIMPLE_SETTINGS = {
        'DYNAMIC_SETTINGS': {
            'backend': 'database',
            'sqlalchemy.url': 'sqlite:///:memory:',
            ...
        }
    }

..

    To install with database dependencies use: ``pip install simple-settings[database]``

Utils
-----

Settings Stub
~~~~~~~~~~~~~

A simple context manager (and decorator) class useful in tests which is
necessary to change some setting in the safe way.

Context Manager example
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from simple_settings import settings
    from simple_settings.utils import settings_stub


    with settings_stub(SOME_SETTING='foo'):
        assert settings.SOME_SETTING == 'foo'
    assert settings.SOME_SETTING == 'bar'

Decorator example
^^^^^^^^^^^^^^^^^

.. code:: python

    from simple_settings import settings
    from simple_settings.utils import settings_stub


    @settings_stub(SOME_SETTING='foo')
    def get_some_setting():
        return settings.SOME_SETTING

    assert get_some_setting() == 'foo'
    assert settings.SOME_SETTING == 'bar'

Changelog
---------

[0.12.0] - 2017-03-07
~~~~~~~~~~~~~~~~~~~~~

-  Load settings from *toml* files.

[0.11.0] - 2017-02-17
~~~~~~~~~~~~~~~~~~~~~

-  Autoconfigure python logging with ``CONFIGURE_LOGGING`` *special
   setting*.

[0.10.0] - 2016-10-28
~~~~~~~~~~~~~~~~~~~~~

-  Support configuring dynamic backends with an optional *prefix*.

[0.9.1] - 2016-09-15
~~~~~~~~~~~~~~~~~~~~

-  ``configure`` method now works even called before the LazySettings
   setup.

[0.9.0] - 2016-08-12
~~~~~~~~~~~~~~~~~~~~

-  ``configure`` method now update settings in dynamic settings.
-  On get setting value in dynamic setting update local settings with
   this value.
-  Auto casting value in dynamic storage to using complex types.

[0.8.1] - 2016-06-04
~~~~~~~~~~~~~~~~~~~~

-  Fix instalation with ``database`` extra requires.

[0.8.0] - 2016-06-04
~~~~~~~~~~~~~~~~~~~~

-  Better ``ImportError`` message if using a dynamic reader without your
   lib dependencies.
-  Refactor in Settings Stub.
-  Dynamic settings behaviors with ``SQLAlchemy`` (``database``
   backend).
-  Load settings of *json* files.

[0.7.0] - 2016-06-02
~~~~~~~~~~~~~~~~~~~~

-  Nice python *REPR* for *LazySettings* objects.
-  Dynamic settings behaviors with ``Redis``.
-  Dynamic settings behaviors with ``Consul``.
-  Generate package with python wheel.

[0.6.0] - 2016-05-17
~~~~~~~~~~~~~~~~~~~~

-  Some refactors.
-  Determine settings files and modules directly in LazySettings object
   (to avoid use env or command line argument).
-  ``configure`` method to update settings.
-  Use ``safe_load`` instead ``load`` in yaml strategy.

[0.5.0] - 2016-02-03
~~~~~~~~~~~~~~~~~~~~

-  Some refactors.
-  Load settings of *yaml* files.
-  New ``SIMPLE_SETTINGS`` environment variable.
-  New ``--simple-settings`` command line arg.

[0.4.0] - 2016-01-03
~~~~~~~~~~~~~~~~~~~~

-  Lazy settings load.

[0.3.1] - 2015-07-23
~~~~~~~~~~~~~~~~~~~~

-  Avoid to load python modules (as settings) in python files (with
   this, fix ``deepcopy`` bug in ``as_dict()`` method).

[0.3.0] - 2015-07-19
~~~~~~~~~~~~~~~~~~~~

-  Deepcopy in ``as_dict`` method to anticipate unexpected changes.
-  Special Settings Behaviors.

   -  Override settings values by environment.
   -  Required settings validation.

-  Remove default behavior of override settings values by environment
   (now it's a special settings).
-  Settings Stub (useful for tests)
-  Change bahavior of settings ``__getattr__`` (before may raise
   ``KeyError`` if simple-settings do not locate the setting, now raise
   ``AttributeError``)

[0.2.0] - 2015-06-19
~~~~~~~~~~~~~~~~~~~~

-  Load multiple settings separated by comma (like a pipeline).
-  Load settings of *cfg* files.
-  Filter python module attributes to read only user settings.

[0.1.1] - 2015-05-19
~~~~~~~~~~~~~~~~~~~~

-  Fix parser\_args error if using simple-settings with others command
   line arguments.

[0.1.0] - 2015-05-14
~~~~~~~~~~~~~~~~~~~~

-  First release.

