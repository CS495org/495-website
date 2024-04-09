from project.celery import app
from interfaces.objs import pg_interface
from accounts.models import Movie, Show, CustomUser
import requests
from django.db.utils import IntegrityError


def get_images():
    try:
        poster_paths = [mv.poster_path for mv in Movie.objects.all()] \
        + [sh.poster_path for sh in Show.objects.all()]
        for path in poster_paths:
            print(path)
            with open('/imgVar/' + str(path), "wb") as f:
                f.write(
                    requests.get("https://image.tmdb.org/t/p/w500/"+path).content
                )
    except Exception as e:
        print(e)


@app.task
def fill_objects():
    for row in pg_interface.get_rows(table_name='"Movies_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "title", "poster_path"])[:20]:
        try:
            Movie.objects.create(id=row.get("id"),
                                 title=row.get("title"),
                                 overview=row.get("overview"),
                                 poster_path=str(row.get("poster_path")).replace("/",''))
            mv_id = row.get("id")
        except IntegrityError as e:
            pass

    for row in pg_interface.get_rows(table_name='"Shows_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "name", "poster_path", "first_air_date"])[:20]:
        try:
            Show.objects.create(id=row.get("id"),
                                title=row.get("name"),
                                overview=row.get("overview"),
                                poster_path=str(row.get("poster_path")).replace("/",''),
                                first_air_date=row.get("first_air_date"))
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