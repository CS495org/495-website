from project.celery import app
from interfaces.objs import pg_interface
from accounts.models import Movie, Show, CustomUser
import requests
from django.db.utils import IntegrityError


# docker run --rm -v img-var:/home/ alpine ls -l /home | grep "^-" | wc -l
def get_images():
    try:
        poster_paths = [mv.poster_path for mv in Movie.objects.all()] \
        + [mv.backdrop_path for mv in Movie.objects.all()] \
        + [sh.poster_path for sh in Show.objects.all()] \
        + [sh.backdrop_path for sh in Show.objects.all()]
        for path in poster_paths:
            # print(path)
            with open('/imgVar/' + str(path), "wb") as f:
                f.write(
                    requests.get("https://image.tmdb.org/t/p/w500/"+path).content
                )

    except Exception as e:
        print(e)


@app.task
def fill_objects():
    if len(Movie.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_movies'):
            try:
                Movie.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("title"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_ids"),
                                    air_date = row.get("release_date"))
            except IntegrityError as e:
                pass

    elif len(Show.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_shows'):
            try:
                Show.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("name"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_ids"),
                                    air_date = row.get("first_air_date")
                                    )
            except IntegrityError as e:
                pass

    get_images()