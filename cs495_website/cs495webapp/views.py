from django.shortcuts import render
from django.http import JsonResponse
from etb_db.DB import Db
from etb_env.ENV import Env

env_interface = Env()
DB_PARAMS = env_interface.get_db_auth()
db_interface = Db(RDBMS='postgres', AUTH = DB_PARAMS)


def hello_world(request):
    return render(request, 'examples/hello.html')

def db_test_endpt(request):
    try:
        rows = db_interface.get_all(table='example_table')
        return JsonResponse(data = {"response" : rows})
    
    except Exception as e:
        return JsonResponse(e, 401)