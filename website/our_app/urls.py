from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("db-test-endpt/", cache_page(60*1)(views.DatabaseView.as_view()), name='db-test-view'),
]