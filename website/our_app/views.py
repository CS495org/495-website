from django.shortcuts import render
from django.http import request, JsonResponse, HttpResponse, HttpRequest
from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.template.exceptions import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
# from our_app.tasks import addfun
from django.views.generic import FormView, UpdateView
# from django.views.generic import UpdateView

from .forms import FavMoviesForm
from django.urls import reverse_lazy

from interfaces.objs import pg_interface, red


class HomePage(View):
    template_name = 'home.html'

    def get(self, request: HttpRequest):
        # addfun.delay()

        query_files = [
            "trending_shows", "top_ten_shows"
        ]

        query_results = {
            file_name : pg_interface.execute_file_query(file_name)\
                        for file_name in query_files
        }

        context: dict[str, dict[str, list[str]]] = {
            file_name : dict() for file_name in query_files
        }

        for key, value in query_results.items():
            context[key]["names"] = [row.get("name") for row in value]
            context[key]["img_ids"] = [row.get("poster_path").replace('/', '') for row in value]

        # print(context)

        return render(request, self.template_name, context=context)




class UpdateFavMoviesView(LoginRequiredMixin, FormView):
    template_name = 'update_movies.html'
    form_class = FavMoviesForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)







class RenderAnyTemplate(View):
    '''class for quickly developing frontend features\n
    will attempt to render html template found at dev_templates/<file_name>.html\n
    to use this: drop your html template in ./templates/dev_templates, then
    go to https://localhost/render-any/<FILE_NAME>\n
    don't include the .html file extension'''

    def get(self, request: HttpRequest, to_render: str) -> HttpResponse:
            file_path = 'render_any/' + to_render + '.html'

            return render(request, file_path)


class RedisView(View):
    '''redis class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''increment page hits, return it as json'''
        try:
            page_hits = red.incr('page_hits')
            return JsonResponse(data = {"response" : f"Page hits: {page_hits}"})

        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})


# class DatabaseView(LoginRequiredMixin, View):
class DatabaseView(View):
    '''database class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''get * from public.example_table'''
        try:
            rows = pg_interface.get_rows(table_name='"Top_Rated_Movies"')
            return JsonResponse(data = {"response" : rows})

        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})