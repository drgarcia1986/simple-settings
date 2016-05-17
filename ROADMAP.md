simple-settings roadmap
=======================

Available for testing
---------------------

Use `pip install git+https://github.com/drgarcia1986/simple-settings.git` to test this features

* Initialize LazySettings with `settings` as parameter:
```python
LazySettings('foo.setting','bar.cfg', 'barz.yml')
```

* `configure` method to update settings:
```python
>>> settings.SOME_CONF
foo
>>> settings.configure(SOME_CONF='bar')
>>> settings.SOME_CONF
bar
```

Read the [documentation](http://simple-settings.readthedocs.org/en/latest/) for more informations.

Next versions
-------------
* Read settings from remote files.
* Dynamic settings (in simple way).
