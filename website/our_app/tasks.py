import random
from celery import shared_task

@shared_task
def add(x, y):
    # Celery recognizes this as the `movies.tasks.add` task
    # the name is purposefully omitted here.
    return x + y