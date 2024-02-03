from django.shortcuts import render
from django.http import request, JsonResponse, HttpResponse, HttpRequest
from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.template.exceptions import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout

from interfaces.objs import db_interface, red

def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')




class RenderAnyTemplate(View):
    '''class for quickly developing frontend features\n
    will attempt to render html template found at dev_templates/<file_name>.html\n
    to use this: drop your html template in ./templates/dev_templates, then
    go to https://localhost/render-any/<FILE_NAME>\n
    don't include the .html file extension'''
    
    def get(self, request: HttpRequest, to_render: str) -> HttpResponse:
            file_path = 'dev_templates/' + to_render + '.html'
            
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


class DatabaseView(View):
    '''database class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''get * from public.example_table'''
        try:
            rows = db_interface.get_all(table='example_table')
            return JsonResponse(data = {"response" : rows})
        
        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})



def hello_world(request: HttpRequest) -> HttpResponse:
    print(request.path)
    return render(request, 'examples/hello.html')