Python Simple Settings
======================
A simple way to manage your project settings.

It is inspired by Django's settings system but is generic for any python project.<br>
With simple-settings you just need specify your settings module in `--settings` arg of command line (or `SIMPLE_SETTINGS` of environment) and all settings will be available in `simple_settings.settings`.

```python
>>> from simple_settings import settings
>>> print(settings.FOO)
'some value in foo'
```

## Installation
simple-settings is available on [Pypi](https://pypi.python.org/pypi/simple-settings).

```bash
$ pip install simple-settings
```

## How this works

simple-settings reads and stores all variables (or constants if you prefer) of a python module that you specify.
For store your settings you need at least one python module.
The objects in this python module, work as a mapping to settings of project, because, for each object in this module,
simple-settings will seek it's value in environment before assuming the value presenting in module.

To specify your settings module you have two approaches, with command line or environment.

For example, imagine that you have a python module for your project settings and this file is in "_settings/development.py_" (a common example).
To load settings of this file you can run your project with command line arg `--settings`:

```bash
$ python app.py --settings=settings.development

```
> simple-settings accepts `--simple-settings` command line arg also

Or set the environment variable `SIMPLE_SETTINGS`:

```bash
$ export SIMPLE_SETTINGS=settings.development
$ python app.py
```

> the `settings` environment variable is deprecated

The `simple_settings.settings` object reads the command line and environment in this order (but simple-settings takes first value it encounters), to know which file to load.

Another option is use class `LazySettings` instead singleton object `settings`.
With `LazySettings` class is possible to determine settings files in object create:
```python
from simple_settings import LazySettings


settings = LazySettings('settings.development')
```
If you don't pass any value in _LazySettings_ init argument, this class follow the same behavior of _settings_ object.


## Example
This is a very dummy example, in real world you would use simple-settings in more complex cases.

### **project_settings.py**

In this example we just store a simple string but any python type is accepted.

```python
SIMPLE_CONF = 'simple'
```
### **app.py**

You don't need specify which setting _simple-settings_ must load, you can do this with command line or environment.

```python
from simple_settings import settings

print(settings.SIMPLE_CONF)
```
### **Run**

You can specify your settings module with command line:
```bash
$ python app.py --settings=project_settings
simple
```
Or environment:
```bash
$ export SIMPLE_SETTINGS=project_settings
$ python app.py
simple
```

Check [examples](https://github.com/drgarcia1986/simple-settings/tree/master/examples), in project repository for more usage samples.

## as_dict()
You can check the loaded settings through method `settings.as_dict()`
```python
>>> settings.as_dict()
{'SIMPLE_CONF': 'simple'}
```

## Types of settings
The simple-settings is prepared to play with the following files types:

* python modules.
* cfg files (simple `key=value` files).
* yaml files.

> To settings-settings load settings of yaml files is necessary install with extras require _yaml_ ex: `pip install simple-settings[yaml]`

## Load multiple settings modules
simple-settings can load more than one setting module without use import approach, just specify yours settings modules separated by comma.
For example:
```bash
$ python app.py --settings=production,amazon,new_relic
```
simple-setting will load all settings modules in order that was specified (`production`-> `amazon` -> `new_relic`) overriding possibles conflicts.

This also work with _LazySettings_ class:
```python
from simple_settings import LazySettings


settings = LazySettings('production', 'amazon', 'new_relic')
```
You can combine any type of settings (_python modules_, _yaml_, etc.).

## Ignored settings
* Python modules:
	* Variables starting with `_`.
* Cfg files:
	* Keys starting with `#`.

## Special Settings
simple-settings has a list of _special settings_ that change behavior os settings load.
This _special settings_ they are part of `SIMPLE_SETTINGS` dict in settings file.

```python
SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
	'REQUIRED_SETTINGS': ('API_TOKEN', 'DB_USER')
}
```
_Special settings is only available with settings based in python modules._

### Override settings value
You can override the values of your settings module with environment variables.
You just need set the _special setting_ `OVERRIDE_BY_ENV` with `True` as value.

```bash
$ export SIMPLE_CONF="simple from env"
$ python app.py --settings=project_settings
simple from env
```
### Required Settings
You can determine a list of mandatory settings, i.e. settings that require a valid value.
For this, set the _sepecial setting_ `REQUIRED_SETTINGS` with a list (or any iterable) of yours required settings.
If any setting of this list have an invalid value (or it's not present in setting file) a `ValueError` is raised with a list of required settings not satify in settings file.

## Utils
### Settings Stub
A simple context manager (and decorator) class useful in tests which is necessary to change some setting in the safe way.

#### Context Manager example
```python
from simple_settings import settings
from simple_settings.utils import settings_stub


with settings_stub(SOME_SETTING='foo'):
    assert settings.SOME_SETTING == 'foo'
assert settings.SOME_SETTING == 'bar'
```

#### Decorator example
```python
from simple_settings import settings
from simple_settings.utils import settings_stub


@settings_stub(SOME_SETTING='foo')
def get_some_setting():
    return settings.SOME_SETTING

assert get_some_setting() == 'foo'
assert settings.SOME_SETTING == 'bar'
```

## Changelog
### [NEXT_RELEASE]
* Some refactors.
* Determine settings files and modules directly in LazySettings object (to avoid use env or command line argument);

### [0.5.0] - 2016-02-03
* Some refactors.
* Load settings of _yaml_ files.
* New `SIMPLE_SETTINGS` environment variable.
* New `--simple-settings` command line arg.

### [0.4.0] - 2016-01-03
* Lazy settings load.

### [0.3.1] - 2015-07-23
* Avoid to load python modules (as settings) in python files (with this, fix `deepcopy` bug in `as_dict()` method).

### [0.3.0] - 2015-07-19
* Deepcopy in `as_dict` method to anticipate unexpected changes.
* Special Settings Behaviors.
    * Override settings values by environment.
    * Required settings validation.
* Remove default behavior of override settings values by environment (now it's a special settings).
* Settings Stub (useful for tests)
* Change bahavior of settings `__getattr__` (before may raise `KeyError` if simple-settings do not locate the setting, now raise `AttributeError`)

### [0.2.0] - 2015-06-19
* Load multiple settings separated by comma (like a pipeline).
* Load settings of _cfg_ files.
* Filter python module attributes to read only user settings.

### [0.1.1] - 2015-05-19
* Fix parser_args error if using simple-settings with others command line arguments.

### [0.1.0] - 2015-05-14
* First release.
