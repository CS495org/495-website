from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("db-test-endpt/", cache_page(60*1)(views.DatabaseView.as_view()), name='db-test-view'),
    path("main/", views.main_view, name='main'),
    path("profile/", views.profile_view, name='profile'),
    path("calendar/", views.calendar_view, name='calendar'),
    path("discover/", views.discover_view, name='discover'),
    path("settings/", views.settings_view, name='settings'),
    path("group/", views.group_view, name='group'),
    path("genre/", views.genre_view, name='genre'),
    path("showprofile/", views.showprofile_view, name='showprofile'),
    path("will/", views.will_view, name='will'),
]