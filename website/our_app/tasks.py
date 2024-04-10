from project.celery import app
from interfaces.objs import pg_interface
from accounts.models import Movie, Show, CustomUser
import requests
from django.db.utils import IntegrityError


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
    if not len(Movie.objects.all()) == 0:
        return

    for row in pg_interface.get_rows(table_name='"Movies_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "title", "poster_path",
                                           "backdrop_path", "genre_ids",
                                           "release_date"])[:20]:
        try:
            Movie.objects.create(id=str(int(row.get("id"))),
                                 title=row.get("title"),
                                 overview=row.get("overview"),
                                 poster_path=str(row.get("poster_path")).replace("/",''),
                                 backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                 genres=row.get("genre_ids"),
                                 air_date = row.get("release_date"))
            # mv_id = row.get("id")
        except IntegrityError as e:
            pass

    for row in pg_interface.get_rows(table_name='"Shows_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "name", "poster_path",
                                           "backdrop_path", "genre_ids",
                                           "first_air_date"])[:20]:
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

    if len(CustomUser.objects.all()) < 2:
        try:
            _new_usr = CustomUser(username='tateb', email='email@email.com',
                                  password=r'pbkdf2_sha256$720000$cRfkFIziOWa16qa9LvYsjy$P2iZiWk50rgncSv/Q3WKM5DTay38UqjxheQiZ5wscy8=')
            _new_usr.save()

        except Exception as e:
            pass


    get_images()

    # return mv_id