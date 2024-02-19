from django.shortcuts import render
from django.http import request, JsonResponse, HttpResponse, HttpRequest
from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.template.exceptions import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

from interfaces.objs import pg_interface, red



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


class DatabaseView(LoginRequiredMixin, View):
    '''database class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''get * from public.example_table'''
        try:
            rows = pg_interface.get_rows(table_name='example_table')
            return JsonResponse(data = {"response" : rows})
        
        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})