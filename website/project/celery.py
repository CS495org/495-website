import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_celery.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


from celery.schedules import crontab

# Below is for illustration purposes. We
# configured so we can adjust scheduling
# in the Django admin to manage all
# Periodic Tasks like below


app.conf.beat_schedule = {
    'multiply-task-crontab': {
        'task': 'multiply_two_numbers',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}