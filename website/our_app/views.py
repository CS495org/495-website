from django.db.models.base import Model as Model
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, RedirectView
from accounts.models import Movie, CustomUser, Show
from django import forms
from typing import Any
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from interfaces.objs import pg_interface

def get_context():
    context = {
        "all_shows" : Show.objects.all(),
        "all_movies" : Movie.objects.all(),
    }

    return context


class HomePage(View):
    template_name = 'home.html'
    def get(self, request: HttpRequest):
        # if len(Movie.objects.all()) == 0:
            # fill_objects()

        # _movie = Movie.objects.get(mv_id)
        # _movie.add_to_user(request.user)

        context = get_context()
        # context['image_files'] = [f"{i}.jpg" for i in range(51)]
        return render(request, self.template_name, context=context)



class RedirectByUserID(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return f"{self.request.user.id}"


# class RedirectByObjectID(LoginRequiredMixin, RedirectView):
#     def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
#         return f"{self.request.}"


def show_list(request):
    return render(request, 'show_list.html', context=get_context())


class ObjectView(View):
    template = "object_view.html"

    def get(self, request: HttpRequest, **kwargs):
        pk = kwargs.get('pk')
        # print(pk, type(pk))
        return render(request, self.template, context= {
            "show" : Show.objects.get(id=pk)
            } )


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