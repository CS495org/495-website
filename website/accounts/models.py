from django.contrib.auth.models import AbstractUser
from django.db import models

# class EntertainmentItem(models.Model):
#     _id = models.CharField()

class Movie(models.Model):
    _id = models.CharField(max_length=38+9,
                           primary_key=True)
    _title = models.TextField()
    _overview = models.TextField()
    _poster_path = models.TextField()
    # _popularity = models.

    def __str__(self):
        return self._title

# id	adult	title	video	overview	genre_ids	media_type	popularity	vote_count	poster_path	release_date	vote_average	backdrop_path	original_title	original_language	"_airbyte_raw_id"	"_airbyte_extracted_at"	"_airbyte_meta"

class Show(models.Model):
    _id = models.CharField(max_length=38+9,
                           primary_key=True)
    _title = models.TextField()
    _overview = models.TextField()
    _poster_path = models.TextField()

    def __str__(self):
        return self._id


class CustomUser(AbstractUser):
    fav_movies = models.ManyToManyField(Movie, blank=True)
    fav_shows = models.ManyToManyField(Show,  blank=True)

    def __str__(self):
        return self.username

    def _add_movie(self, movie_id: str):
        _mv = Movie(_id = movie_id)
        _mv.save()
        self.fav_movies.add(_mv)

    def _add_show(self, show_id: str):
        _sh = Show(_id=show_id)
        _sh.save()
        self.fav_shows.add(_sh)