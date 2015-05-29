Python Simple Settings
======================
[![Documentation Status](https://readthedocs.org/projects/simple-settings/badge/?version=latest)](http://simple-settings.readthedocs.org/en/latest/)
[![Code Issues](http://www.quantifiedcode.com/api/v1/project/1b5307f0f1584c3b9c736f976b57e973/badge.svg)](http://www.quantifiedcode.com/app/project/1b5307f0f1584c3b9c736f976b57e973)
[![Build Status](https://travis-ci.org/drgarcia1986/simple-settings.svg)](https://travis-ci.org/drgarcia1986/simple-settings)
[![Coverage Status](https://coveralls.io/repos/drgarcia1986/simple-settings/badge.svg)](https://coveralls.io/r/drgarcia1986/simple-settings)

A simple way to manage your project settings.

It is inspired by Django's settings system but is generic for any python project.<br>
With simple-settings you just need specify your settings module in `--settings` arg of command line (or `settings` of environment) and all settings will be available in `simple_settings.settings`.

### Installation
Use `pip` (simple like this project :smile:).

```bash
$ pip install simple-settings
```

### Usage
```bash
$ python app.py --settings=my_settings
```

```python
from simple_settings import settings


print settings.FOO
```

### Quick links
 - [Documentation](http://simple-settings.readthedocs.org/en/latest/)
 - [Examples](https://github.com/drgarcia1986/simple-settings/tree/master/examples)
 - [Roadmap](https://github.com/drgarcia1986/simple-settings/tree/master/ROADMAP.md)
