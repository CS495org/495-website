from django.shortcuts import render
from django.http import request, JsonResponse, HttpResponse
from redis import Redis

from etb_db.DB import Db
from etb_env.ENV import Env


env_interface = Env()
DB_PARAMS = env_interface.get_db_auth()
db_interface = Db(RDBMS='postgres', AUTH = DB_PARAMS)

red = Redis(host='redis', port=6379)


def hello_world(request: request) -> HttpResponse:
    return render(request, 'examples/hello.html')


def db_test_endpt(request: request) -> JsonResponse:
    try:
        rows = db_interface.get_all(table='example_table')
        return JsonResponse(data = {"response" : rows})
    
    except Exception as e:
        return JsonResponse(data = {"error" : e})
    

def redis_test_endpt(request: request) -> JsonResponse:
    try:
        page_hits = red.incr('page_hits')
        return JsonResponse(data = {"response" : f"Page hits: {page_hits}"})
    
    except Exception as e:
        return JsonResponse(data = {"error" : e})
