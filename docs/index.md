Python Simple Settings
======================
A simple way to manage your project settings.

It is inspired by Django's settings system but is generic for any python project.<br>
With simple-settings you just need specify your settings module in `--settings` arg of command line (or `settings` of environment) and all settings will be available in `simple_settings.settings`.

```python
from simple_settings import settings


print settings.FOO
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

Or set the environment variable `settings`:

```bash
$ export settings=settings.development
$ python app.py
```
The `simple_settings.settings` object reads the command line and environment in this order (but simple-settings takes first value it encounters), to know which file to load.


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

print settings.SIMPLE_CONF
```
### **Run**

You can specify your settings module with command line:
```bash
$ python app.py --settings=project_settings
simple
```
Or environment:
```bash
$ export settings=project_settings
$ python app.py
simple
```
### **Override settings value**

You can override the values of your settings module with environment variables.

```bash
$ export SIMPLE_CONF="simple from env"
$ python app.py --settings=project_settings
simple from env
```
Check [examples](https://github.com/drgarcia1986/simple-settings/tree/master/examples), in project repository for more usage samples.

## Load multiple settings modules
simple-settings can load more than one setting module without use import approach, just specify yours settings modules separated by comma.
For example:
```bash
$ python app.py --settings=production,amazon,new_relic
```
simple-setting will load all settings modules in order that was specified (`production`-> `amazon` -> `new_relic`) overriding possibles conflicts.

But remember, the environment is still a priority. 

## Changelog

### [NEXT_RELEASE]
 - Load multiple settings separated by comma (like a pipeline).
 - Load settings of _cfg_ files.

### [0.1.1] - 2015-05-19
 - Fix parser_args error if using simple-settings with others command line arguments.

### [0.1.0] - 2015-05-14
 - First release.
