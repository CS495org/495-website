from django.contrib.auth.models import AbstractUser
from django.db import models

# class EntertainmentItem(models.Model):
#     _id = models.CharField()

class Movie(models.Model):
    id = models.CharField(max_length=38+9,
                           primary_key=True)
    title = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    air_date = models.DateField()
    genres = models.TextField()

    def add_to_user(self, user):
        _user = CustomUser.objects.get(user)
        _user.add_movie(self.id)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "title" : self.title,
            "overview" : self.overview,
            "id" : self.id,
            "poster_path" : self.poster_path,
        }

# id	adult	title	video	overview	genre_ids	media_type	popularity	vote_count	poster_path	release_date	vote_average	backdrop_path	original_title	original_language	"_airbyte_raw_id"	"_airbyte_extracted_at"	"_airbyte_meta"

class Show(models.Model):
    id = models.CharField(max_length=38+9,
                           primary_key=True)
    title = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    air_date = models.DateField()
    genres = models.TextField()

    def add_to_user(self, user):
        _user = CustomUser.objects.get(user)
        _user.add_show(self.id)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "title" : self.title,
            "overview" : self.overview,
            "id" : self.id,
            "poster_path" : self.poster_path,
        }

class TopRatedShow(models.Model):
    id = models.CharField(max_length=38+9,
                           primary_key=True)
    title = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    air_date = models.DateField()
    genres = models.TextField()

    def add_to_user(self, user):
        _user = CustomUser.objects.get(user)
        _user.add_show(self.id)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "title" : self.title,
            "overview" : self.overview,
            "id" : self.id,
            "poster_path" : self.poster_path,
        }


class CustomUser(AbstractUser):
    '''
    fav_movies = models.ManyToManyField(Movie, blank=True)
    fav_shows = models.ManyToManyField(Show, blank=True)
    fav_top_rated = models.ManyToManyField(TopRatedShow, blank=True)
    comp_shows = models.ManyToManyField(Show, blank=True)
    comp_top_rated = models.ManyToManyField(TopRatedShow, blank=True)
    '''

    fav_movies = models.ManyToManyField(Movie, blank=True)
    fav_shows = models.ManyToManyField(Show, related_name='favorited_by', blank=True)
    fav_top_rated = models.ManyToManyField(TopRatedShow, related_name='favorited_by', blank=True)
    comp_shows = models.ManyToManyField(Show, related_name='completed_by', blank=True)
    comp_top_rated = models.ManyToManyField(TopRatedShow, related_name='completed_by', blank=True)
    watch_shows = models.ManyToManyField(Show, related_name='watchlist_by', blank=True)
    watch_top_rated = models.ManyToManyField(TopRatedShow, related_name='watchlist_by', blank=True)

    def __str__(self):
        return self.username

    def add_movie(self, movie_id: str):
        _mv = Movie(_d = movie_id)
        _mv.save()
        self.fav_movies.add(_mv)

    def add_show(self, show_id: str):
        _sh = Show(id=show_id)
        _sh.save()
        self.fav_shows.add(_sh)

    def add_top(self, show_id: str):
        _to = TopRatedShow(id=show_id)
        _to.save()
        self.fav_top_rated.add(_to)

    def add_comp_show(self, show_id: str):
        _sc = Show(id=show_id)
        _sc.save()
        self.comp_shows.add(_sh)

    def add_comp_top(self, show_id: str):
        _tc = TopRatedShow(id=show_id)
        _tc.save()
        self.comp_top_rated.add(_to)
