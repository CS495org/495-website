from django.apps import AppConfig



class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


    # def ready(self) -> None:
    #     from interfaces.objs import pg_interface
    #     from .models import Movie
    #     for row in pg_interface.get_rows(table_name='"Movies_Trending_This_Week"',
    #                                      cols=["id"]):
    #         Movie.objects.create(_id=row.get("id"))

    #     return super().ready()