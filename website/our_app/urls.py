from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("db-test-endpt/", views.DatabaseView.as_view(), name='db-test-view')
]