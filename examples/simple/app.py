import os

from simple_settings import settings

os.environ.setdefault('SIMPLE_SETTINGS', 'project_settings')

print(settings.SIMPLE_CONF)
