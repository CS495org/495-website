from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, RedirectView
from accounts.models import Movie, CustomUser, Show, TopRatedShow
from django import forms
from typing import Any
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from datetime import datetime
from django.http import JsonResponse

from interfaces.objs import pg_interface

def get_context():
    context = {
        "all_shows" : Show.objects.all(),
        "all_movies" : Movie.objects.all(),
        "top_rated_shows": TopRatedShow.objects.all()
    }

    return context

@login_required
def home_view(request):
    context = get_context()

    if request.user.is_authenticated:
        fav_shows = request.user.fav_shows.all()
        fav_show_ids = set(fav_shows.values_list('id', flat=True))
        context.update({
            'fav_shows': fav_shows,
            'fav_show_ids': fav_show_ids,
        })

    #context = get_context()
    
    return render(request, "home.html", context=context)


class HomePage(View):
    template_name = 'home.html'

    '''
    def get(self, request: HttpRequest):
        # if len(Movie.objects.all()) == 0:
            # fill_objects()

        # _movie = Movie.objects.get(mv_id)
        # _movie.add_to_user(request.user)

        return render(request, self.template_name, context=context)
    '''

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect to home_view
            return redirect('home')  # Adjust 'home_view' to your actual view name
        else:
            context = get_context()
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

class AjaxUpdateFavShowsView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                show = Show.objects.get(pk=show_id)
                if user.fav_shows.filter(pk=show_id).exists():  # Check if the show is already favorited
                    user.fav_shows.remove(show)  # Remove the show from fav_shows
                    action = 'removed'
                else:
                    user.fav_shows.add(show)  # Add the show to fav_shows
                    action = 'added'
                user.save()

                fav_show_ids = list(user.fav_shows.values_list('id', flat=True))
                

                return JsonResponse({'action': action, 'fav_show_ids': fav_show_ids})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Show ID is required.'}, status=400)

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **get_context()}


def main_view(request):
    return render(request, "main.html", get_context())


@login_required
def profile_view(request):
    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    context = {
        'fav_shows': fav_shows,  # Pass the user's favorited shows to the template
        'fav_show_ids': fav_show_ids,
        **get_context()
    }
    return render(request, "accounts/profile.html", context)

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

def showprofile_view(request, show_id):
    try:
        # Try to get the Show object first
        show = Show.objects.get(id=show_id)
    except Show.DoesNotExist:
        try:
            # If the Show object does not exist, try to get the TopRatedShow object
            show = TopRatedShow.objects.get(id=show_id)
        except TopRatedShow.DoesNotExist:
            # If neither Show nor TopRatedShow object exists, return a 404 error
            return HttpResponseNotFound("Show not found")
    
    context = {'show': show}
    return render(request, 'accounts/showprofile.html', context)

def will_view(request):
    return render(request, "group/will.html", get_context())