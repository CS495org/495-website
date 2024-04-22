from project.celery import app
from interfaces.objs import pg_interface, env, pg_writer
from accounts.models import Movie, Show, TopRatedShow
import requests
from django.db.utils import IntegrityError


# docker run --rm -v img-var:/home/ alpine ls -l /home | grep "^-" | wc -l
# run this ^^ to see how many pictures you have in the volume
@app.task
def get_images():
    try:
        for _list in (TopRatedShow.objects.filter(images_loaded=False),
                      Show.objects.filter(images_loaded=False),
                      Movie.objects.filter(images_loaded=False)):
            for obj in _list:
                for path in {obj.poster_path, obj.backdrop_path}:
                    with open('/imgVar/' + str(path), "wb") as f:
                        f.write(
                            requests.get("https://image.tmdb.org/t/p/w500/"+path).content
                        )
                obj.images_loaded = True

    except Exception as e:
        print(e)


@pg_writer.str_to_query
def insert_genre(id: int, genre_name: str):
    return f"insert into genre_map values ({id}, {genre_name})"


@app.task
def fill_objects():
    try:
        pg_interface.execute_str_query('select 1 from genre_map')
    except Exception as e:
        pg_interface.__connection__.commit()
        pg_writer.execute_file_query('create_genres')
        TMDB_KEY = env.get(["TMDB_API_KEY"]).get("TMDB_API_KEY")

        r = requests.get(
            f'https://api.themoviedb.org/3/genre/tv/list?api_key={TMDB_KEY}&language=en-US',
            headers={"accept": "application/json"})

        for genre in r.json().get("genres"):
            insert_genre(genre.get("id"), f"'{genre.get('name')}'")


    if len(Movie.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_movies')[20:]:
            try:
                Movie.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("title"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_names"),
                                    air_date = row.get("release_date"))
            except IntegrityError as e:
                pass

    if len(Show.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_shows')[20:]:
            try:
                Show.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("name"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_names"),
                                    air_date = row.get("first_air_date"),
                                    vote_count=row.get("vote_count"),
                                    vote_average=row.get("vote_average"),
                                    )
            except IntegrityError as e:
                pass

    if len(TopRatedShow.objects.all()) == 0:
        for row in pg_interface.execute_file_query('init_top_shows')[20:]:
            try:
                TopRatedShow.objects.create(id=str(int(row.get("id"))),
                                    title=row.get("name"),
                                    overview=row.get("overview"),
                                    poster_path=str(row.get("poster_path")).replace("/",''),
                                    backdrop_path = str(row.get("backdrop_path")).replace("/", ""),
                                    genres=row.get("genre_names"),
                                    air_date = row.get("first_air_date")
                                    )
            except IntegrityError as e:
                pass

    # get_images()