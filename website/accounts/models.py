from django.contrib.auth.models import AbstractUser
from django.db import models

# class EntertainmentItem(models.Model):
#     _id = models.CharField()

class Movie(models.Model):
    _id = models.CharField()
    pass
    # _id = models.CharField()

class Show(models.Model):
    _id = models.CharField()
    pass


class CustomUser(AbstractUser):
    fav_movies = models.ManyToManyField(Movie, blank=True)
    fav_shows = models.ManyToManyField(Show,  blank=True)

    def __str__(self):
        return self.username