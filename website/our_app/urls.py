from django.urls import path
from django.views.decorators.cache import cache_page
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path("db-test-endpt/", cache_page(60*1)(views.DatabaseView.as_view()), name='db-test-view'),
    path('update-fav-movies/<slug:pk>/', views.UpdateFavMoviesView.as_view(), name='update_fav_movies'),
    path('update-fav-movies/', views.RedirectByUserID.as_view(), name='update_movies_redirect'),
    path('update-fav-shows/<slug:pk>/', views.UpdateFavShowsView.as_view(), name='update_fav_shows'),
    path('update-fav-shows/', views.RedirectByUserID.as_view(), name='update_shows_redirect'),
    path('shows/', views.show_list, name="all_shows"),
    path('any-show/<slug:pk>/', views.ObjectView.as_view(), name='object_view'),
    # path('any-show/', views.RedirectByObjectID.as_view(), name='object_view_redirect'),

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
