Python Simple Settings
======================
[![Code Issues](http://www.quantifiedcode.com/api/v1/project/1b5307f0f1584c3b9c736f976b57e973/badge.svg)](http://www.quantifiedcode.com/app/project/1b5307f0f1584c3b9c736f976b57e973)
[![Build Status](https://travis-ci.org/drgarcia1986/simple-settings.svg)](https://travis-ci.org/drgarcia1986/simple-settings)
[![Coverage Status](https://coveralls.io/repos/drgarcia1986/simple-settings/badge.svg)](https://coveralls.io/r/drgarcia1986/simple-settings)

A simple way to manage your project settings.

With `simple_settings` you just need specify your settings module in `--settings` arg (of command line or enviroment) and all will be available in `simple_settings.settings`.

### Instalation
Use `pip` (simple like this project :smile:).

```bash
$ pip install simple-settings
```

### Usage
#### _project_settings.py_
```python
# -*- coding: utf-8 -*-
SIMPLE_CONF = 'simple'
```
#### _app.py_
```python
# -*- coding: utf-8 -*-
from simple_settings import settings

print settings.SIMPLE_CONF
```
#### _Run_
With command line args
```bash
$ python app.py --settings=project_settings
simple
```
Or env
```bash
$ export settings=project_settings
$ python app.py
simple
```
Check [examples](https://github.com/drgarcia1986/simple-settings/tree/master/examples) for more usage samples.
