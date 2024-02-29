import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


from celery.schedules import crontab

# Below is for illustration purposes. We
# configured so we can adjust scheduling
# in the Django admin to manage all
# Periodic Tasks like below


app.conf.beat_schedule = {
    'multiply-task-crontab': {
        'task': 'our_app.tasks.addfun',
        'schedule': 30.0,
        'args': (16, 16),
    },
}