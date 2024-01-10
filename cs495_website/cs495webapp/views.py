from django.shortcuts import render

# Create your views here.
# hello/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("<h1>Hello, World!</h1>")
