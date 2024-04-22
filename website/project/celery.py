import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(broker_connection_retry_on_startup=True)
app.autodiscover_tasks()


beat_schedule = {
    'fill-movie-objects' : {
        'task' : 'our_app.tasks.fill_objects',
        'schedule' : 30.0
    },
    'fill-images' : {
        'task' : 'our_app.tasks.get_images',
        'schedule' : 10.0
    }
}

