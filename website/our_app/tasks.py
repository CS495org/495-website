from celery import shared_task
# from celery import ta

@shared_task
def addfun(x, y):
    # Celery recognizes this as the `movies.tasks.add` task
    # the name is purposefully omitted here.
    print('\n\nCELERY WORKING\n\n')
    return x + y