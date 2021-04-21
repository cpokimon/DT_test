import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project', broker='redis://redis:6379/0', task_serializer='json')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(['news'])

app.conf.timezone = 'UTC'
