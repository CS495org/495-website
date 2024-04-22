from project.celery import app
from interfaces.objs import pg_interface
from accounts.models import Movie, Show, CustomUser
import requests
from django.db.utils import IntegrityError


@app.task
def get_images():
    try:
        poster_paths = [sh.poster_path for sh in Show.objects.all()] \
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
    if len(Show.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_shows')[:500]:
            try:
                Show.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("name"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path=str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_ids"),
                                    air_date = row.get("first_air_date"),
                                    vote_count=row.get("vote_count"),
                                    vote_average=row.get("vote_average")
                                    )
            except IntegrityError as e:
                pass

    get_images()