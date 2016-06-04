# -*- coding: utf-8 -*-
from .base import BaseReader

try:
    from sqlalchemy import engine_from_config, Column, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "database" dynamic settings reader\n'
        'you need to install simple-settings with database dependency:\n'
        'pip install simple-settings[database] or pip install SQLAlchemy'
    )


Base = declarative_base()


class SimpleSettings(Base):
    __tablename__ = 'simple_settings'

    key = Column(String, primary_key=True)
    value = Column(String, primary_key=True)


class DatabaseOperations(object):

    def __init__(self, database_config):
        self.db = engine_from_config(database_config)

        Session = sessionmaker(bind=self.db)
        self.session = Session()

        Base.metadata.create_all(self.db)

    def set(self, key, value):
        setting = SimpleSettings(key=key, value=value)

        self.session.add(setting)
        self.session.commit()

    def get(self, key):
        data = self.session.query(SimpleSettings).filter_by(key=key).first()

        if data:
            return data.value

    def delete(self, key):
        self.session.query(SimpleSettings).filter_by(key=key).delete()
        self.session.commit()

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
