from django.urls import path
from django.views.decorators.cache import cache_page
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("db-test-endpt/", cache_page(60*1)(views.DatabaseView.as_view()), name='db-test-view'),
    path('update-fav-movies/<slug:pk>/', views.UpdateFavMoviesView.as_view(), name='update_fav_movies'),
    path('update-fav-movies/', views.RedirectToUpdateMovies.as_view(), name='update_movies_redirect')
]