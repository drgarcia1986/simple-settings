# -*- coding: utf-8 -*-
from .base import BaseReader

try:
    from sqlalchemy import engine_from_config, Column, String
    from sqlalchemy.ext.declarative import as_declarative
    from sqlalchemy.orm import sessionmaker
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "database" dynamic settings reader\n'
        'you need to install simple-settings with database dependency:\n'
        'pip install simple-settings[database] or pip install SQLAlchemy'
    )


@as_declarative()
class Base(object):
    """Base class for declarative class definitions
    """


class SimpleSettings(Base):
    """Database table representation
    """

    __tablename__ = 'simple_settings'

    key = Column(String, primary_key=True)
    value = Column(String)


class DatabaseOperations(object):
    """Wrapper for database operations
    """

    def __init__(self, database_config):
        self.db = engine_from_config(database_config)

        self.session = sessionmaker(bind=self.db)()

        Base.metadata.create_all(self.db)

    def _get(self, key):
        return self.session.query(SimpleSettings).get(key)

    def set(self, key, value):
        setting = self._get(key)
        if not setting:
            setting = SimpleSettings(key=key)
        setting.value = value

        self.session.add(setting)
        self.session.commit()

    def get(self, key):
        data = self._get(key)

        if data:
            return data.value

    def flush(self):
        self.session.query(SimpleSettings).delete()
        self.session.commit()


class Reader(BaseReader):
    """
    Database settings Reader
    A simple orm using getter
    """
    _default_conf = {
        'sqlalchemy.url': 'sqlite:///:memory:'
    }

    def __init__(self, conf):
        super(Reader, self).__init__(conf)

        self.db = DatabaseOperations(self.conf)

    def _get(self, key):
        return self.db.get(key)

    def _set(self, key, value):
        self.db.set(key, value)
