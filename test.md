# Testing

Our approach to testing focuses heavily on unit testing the Django web application. Unit tests are contained in /website/our_app/tests.py and /website/accounts/tests.py. The testing isn't totally complete, but you'll find a variety of tests checking our TV show, movie, and CustomUser models, along with tests for the views.

To run the tests, first spin up the containers with "./all.sh" from the repo root. Then, after you see that the tv-web container has started the task queue (the last step of initializing the application), enter the web container from the command line with:

```docker exec -it tv-web sh```

To run the tests, run:

```python manage.py test```


How do you know that the task queue has been started successfully? You'll see logs like this in the command line where you ran "./all.sh".
```
tv-web    | [2024-04-24 03:14:49,720: INFO/ForkPoolWorker-5] Task our_app.tasks.get_images[d15505f2-cc2d-4723-8cbe-93185ab81a64] succeeded in 0.032018587007769383s: None
```


The tests run on a separate SQLite3 database. This is an ephemeral, single file database that is torn down when the container exits.