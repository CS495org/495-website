from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/", views.group_view, name="group"),
    path("group/reggie", views.reggie_view, name="reggie"),
    path("group/reiland", views.reiland_view, name="reiland"),
    path("group/tate", views.tate_view, name="tate"),
    path("group/will", views.will_view, name="will"),
]
