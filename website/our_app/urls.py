from django.urls import path
from django.views.decorators.cache import cache_page
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path("db-test-endpt/", cache_page(60*1)(views.DatabaseView.as_view()), name='db-test-view'),
    path('update-fav-movies/<slug:pk>/', views.UpdateFavMoviesView.as_view(), name='update_fav_movies'),
    path('update-fav-movies/', views.RedirectToUpdateMovies.as_view(), name='update_movies_redirect'),
    path('update-fav-shows/<slug:pk>/', views.UpdateFavShowsView.as_view(), name='update_fav_shows'),
    path('update-fav-shows/', views.RedirectToUpdateShows.as_view(), name='update_shows_redirect'),
    path('shows/', views.show_list, name="all_shows"),
    # path('shows/', views.show_list, name='show_list'),
    # path('add_favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    # path('update_favorite/<int:pk>/', views.update_favorite, name='update_favorite'),
    # path('delete_favorite/<int:pk>/', views.delete_favorite, name='delete_favorite'),
    # Add similar URLs for movies
]
