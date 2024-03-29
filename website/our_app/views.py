from django.db.models.base import Model as Model
from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, RedirectView
from accounts.models import Movie, CustomUser, Show
from django import forms
from typing import Any
from django.db.utils import IntegrityError
from django.urls import reverse_lazy

from interfaces.objs import pg_interface

def get_context():
    context = {
        "all_shows" : Show.objects.all(),
        "all_movies" : Movie.objects.all(),
    }

    return context

def fill_objects():
    for row in pg_interface.get_rows(table_name='"Movies_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "title", "poster_path"])[:20]:
        try:
            Movie.objects.create(id=row.get("id"),
                                 title=row.get("title"),
                                 overview=row.get("overview"),
                                 poster_path=str(row.get("poster_path")).replace("/",''))
        except IntegrityError as e:
            pass

    for row in pg_interface.get_rows(table_name='"Shows_Trending_This_Week"',
                                     cols=["id", "overview",
                                           "name", "poster_path"])[:20]:
        try:
            Show.objects.create(id=row.get("id"),
                                title=row.get("name"),
                                overview=row.get("overview"),
                                poster_path=str(row.get("poster_path")).replace("/",''))
        except IntegrityError as e:
            pass

    if len(CustomUser.objects.all()) < 2:
        try:
            _new_usr = CustomUser(username='tateb', email='email@email.com',
                                  password=r'pbkdf2_sha256$720000$cRfkFIziOWa16qa9LvYsjy$P2iZiWk50rgncSv/Q3WKM5DTay38UqjxheQiZ5wscy8=')
            _new_usr.save()

        except Exception as e:
            pass


class HomePage(View):
    template_name = 'home.html'
    def get(self, request: HttpRequest):
        if len(Movie.objects.all()) == 0:
             fill_objects()

        context = get_context()
        # context['image_files'] = [f"{i}.jpg" for i in range(51)]
        return render(request, self.template_name, context=context)



class RedirectByID(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return f"{self.request.user.id}"


def show_list(request):
    return render(request, 'show_list.html', context=get_context())


class UpdateFavMoviesView(LoginRequiredMixin, UpdateView):
    template_name = 'update_movies.html'
    success_url = reverse_lazy('home')
    model = CustomUser

    fields = ['fav_movies']
    _movie = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    queryset = CustomUser.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return {**context, **get_context()}



class UpdateFavShowsView(LoginRequiredMixin, UpdateView):
    template_name = 'update_shows.html'
    success_url = reverse_lazy('home')
    model = CustomUser

    fields = ['fav_shows']
    _show = forms.ModelMultipleChoiceField(
        queryset=Show.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    queryset = CustomUser.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return {**context, **get_context()}



def main_view(request):
    return render(request, "main.html", get_context())

def profile_view(request):
    return render(request, "accounts/profile.html", get_context())

def calendar_view(request):
    return render(request, "accounts/calendar.html", get_context())

def discover_view(request):
    return render(request, "accounts/discover.html", get_context())

def settings_view(request):
    return render(request, "accounts/settings.html", get_context())

def group_view(request):
    return render(request, "accounts/group.html", get_context())

def genre_view(request):
    context = get_context()
    context["image_files"] = [f"{i}.jpg" for i in range(51)]
    return render(request, "accounts/genre.html", context)

def showprofile_view(request):
    return render(request, "accounts/showprofile.html", get_context())

def will_view(request):
    return render(request, "group/will.html", get_context())