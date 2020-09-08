import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
from otree.management.cli import execute_from_command_line
from django.conf import settings as django_settings
from otree_startup import configure_settings, do_django_setup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']
try:
    configure_settings(DJANGO_SETTINGS_MODULE)
    do_django_setup()
except RuntimeError:
    print('apparatenly called by django?')

app = Celery('o')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
