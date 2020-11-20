import os
from pathlib import Path
from celery import Celery
from importlib import import_module
from django.conf import settings as django_settings
from otree_startup import augment_settings, do_django_setup


def configure_settings(DJANGO_SETTINGS_MODULE: str = 'settings'):
    user_settings_module = import_module(DJANGO_SETTINGS_MODULE)
    user_settings_dict = {}
    user_settings_dict['BASE_DIR'] = os.path.dirname(
        os.path.abspath(user_settings_module.__file__)
    )
    # this is how Django reads settings from a settings module
    for setting_name in dir(user_settings_module):
        if setting_name.isupper():
            setting_value = getattr(user_settings_module, setting_name)
            user_settings_dict[setting_name] = setting_value

    # find the correct path of the sqlite database file
    current_path = Path(os.path.dirname(__file__))
    db_path = os.path.join(current_path.parent, "db.sqlite3")

    default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_path,
    }


    augment_settings(user_settings_dict)
    user_settings_dict['DATABASES'] = {'default': default_db}
    django_settings.configure(**user_settings_dict)


# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
from otree.management.cli import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']

try:
    configure_settings(DJANGO_SETTINGS_MODULE)
    print("SETTINGS CONFIGURED")
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
