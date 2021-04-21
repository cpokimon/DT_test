import os
from celery import Celery
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

app = Celery('project')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(['news'])

app.conf.beat_schedule = {
    'do-something-periodically': {
        'task': 'reset_upvoutes',
        'schedule': 3.0,
    },
}

app.conf.timezone = 'UTC'
