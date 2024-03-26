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

from interfaces.objs import pg_interface, red


class HomePage(View):
    template_name = 'home.html'

    def get(self, request: HttpRequest):
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

        # testing something #########################################################
        #image_files = ['0.jpg', '1.jpg', '2.jpg']
        image_files = [f"{i}.jpg" for i in range(51)]
        context['image_files'] = image_files

        return render(request, self.template_name, context=context)


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


def main_view(request):
    return render(request, "main.html")

def profile_view(request):
    return render(request, "accounts/profile.html")

def calendar_view(request):
    return render(request, "accounts/calendar.html")

def discover_view(request):
    return render(request, "accounts/discover.html")

def settings_view(request):
    return render(request, "accounts/settings.html")

def group_view(request):
    return render(request, "accounts/group.html")

def genre_view(request):
    image_files = [f"{i}.jpg" for i in range(51)]
    return render(request, "accounts/genre.html", {'image_files': image_files})

def showprofile_view(request):
    return render(request, "accounts/showprofile.html")