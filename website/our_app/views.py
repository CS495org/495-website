from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, RedirectView
from accounts.models import Movie, CustomUser, Show
from django import forms
from typing import Any
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import random
from django.db.models import Q

from datetime import datetime
from django.http import JsonResponse

from interfaces.objs import pg_interface

def get_context():
    top_ten_shows = Show.objects.order_by('-vote_count')[:10]

    context = {
        "all_shows" : Show.objects.all(),
        "all_movies" : Movie.objects.all(),
        'top_ten_shows': top_ten_shows
    }

    return context


# @login_required
def home_view(request):
    context = get_context()

    if request.user.is_authenticated:
        fav_shows = request.user.fav_shows.all()
        fav_show_ids = set(fav_shows.values_list('id', flat=True))

        comp_shows = request.user.comp_shows.all()
        comp_show_ids = set(comp_shows.values_list('id', flat=True))

        watch_shows = request.user.watch_shows.all()
        watch_show_ids = set(watch_shows.values_list('id', flat=True))

        top_ten_shows = Show.objects.order_by('-vote_count')[:10]

        context.update({
            'fav_shows': fav_shows,
            'fav_show_ids': fav_show_ids,
            'comp_shows': comp_shows,
            'comp_show_ids': comp_show_ids,
            'watch_shows': watch_shows,
            'watch_show_ids': watch_show_ids,
            'top_ten_shows': top_ten_shows

        })


    return render(request, "home.html", context=context)



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


class AjaxUpdateCompShowsView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                show = Show.objects.get(pk=show_id)
                if user.comp_shows.filter(pk=show_id).exists():  # Check if the show is already favorited
                    user.comp_shows.remove(show)  # Remove the show from fav_shows
                    action_comp_show = 'removed'
                else:
                    user.comp_shows.add(show)  # Add the show to fav_shows
                    action_comp_show = 'added'
                user.save()

                comp_show_ids = list(user.comp_shows.values_list('id', flat=True))


                return JsonResponse({'action_comp_show': action_comp_show, 'comp_show_ids': comp_show_ids})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Show ID is required.'}, status=400)

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **get_context()}


class AjaxUpdateWatchShowsView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                show = Show.objects.get(pk=show_id)
                if user.watch_shows.filter(pk=show_id).exists():  # Check if the show is already favorited
                    user.watch_shows.remove(show)  # Remove the show from fav_shows
                    action_watch_show = 'removed'
                else:
                    user.watch_shows.add(show)  # Add the show to fav_shows
                    action_watch_show = 'added'
                user.save()

                watch_show_ids = list(user.watch_shows.values_list('id', flat=True))


                return JsonResponse({'action_watch_show': action_watch_show, 'watch_show_ids': watch_show_ids})
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
    context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    context.update({
        'fav_shows': fav_shows,
        'fav_show_ids': fav_show_ids,
        'comp_shows': comp_shows,
        'comp_show_ids': comp_show_ids,
        'watch_shows': watch_shows,
        'watch_show_ids': watch_show_ids
    })

    return render(request, "accounts/profile.html", context)

@login_required
def calendar_view(request):
    return render(request, "accounts/calendar.html", get_context())

@login_required
def discover_view(request):
    context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    most_recent_shows = Show.objects.order_by('-air_date')[:10]

    #Because you favorited...
    if fav_shows.exists() and fav_shows.first().genres:
        first_show = fav_shows.last()
        first_genres_fav = first_show.genres

        query = Q(genres__contains=first_genres_fav[0])
        for genre_id in first_genres_fav[1:]:
            query |= Q(genres__contains=genre_id)

        # Fetch matching shows' IDs
        matching_show_ids = (
            Show.objects.filter(query)
            .values_list('id', flat=True)
        )

        # Convert QuerySet to list and shuffle the IDs
        matching_show_ids = list(matching_show_ids)
        random.shuffle(matching_show_ids)

        # Retrieve 20 shows based on the shuffled IDs
        matching_shows = Show.objects.filter(id__in=matching_show_ids[:20])
    else:
        first_show = None
        first_genres_fav = None
        matching_shows = []


    #Because you completed...
    if comp_shows.exists() and comp_shows.first().genres:
        first_comp = comp_shows.first()
        first_genres_comp = first_comp.genres

        query = Q(genres__contains=first_genres_comp[0])
        for genre_id in first_genres_comp[1:]:
            query |= Q(genres__contains=genre_id)

        # Fetch matching watched shows' IDs
        matching_comp_ids = (
            Show.objects.filter(query)
            .values_list('id', flat=True)
        )

        # Convert QuerySet to list and shuffle the IDs
        matching_comp_ids = list(matching_comp_ids)
        random.shuffle(matching_comp_ids)

        # Retrieve 20 watched shows based on the shuffled IDs
        matching_comp = Show.objects.filter(id__in=matching_comp_ids[:20])
    else:
        first_comp = None
        first_genres_comp = None
        matching_comp = []


    context.update({
        'fav_shows': fav_shows,
        'fav_show_ids': fav_show_ids,
        'comp_shows': comp_shows,
        'comp_show_ids': comp_show_ids,
        'watch_shows': watch_shows,
        'watch_show_ids': watch_show_ids,
        'most_recent_shows': most_recent_shows,
        'matching_shows' : matching_shows,
        'first_show' : first_show,
        'matching_comp' : matching_comp,
        'first_comp' : first_comp,
    })

    return render(request, "accounts/discover.html", context)


@login_required
def settings_view(request):
    return render(request, "accounts/settings.html", get_context())

def group_view(request):
    return render(request, "accounts/group.html", get_context())

@login_required
def genre_view(request, genre_id, genre_name):
    context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    crime_shows = Show.objects.filter(genres__contains=[9648])
    action_shows = Show.objects.filter(genres__contains=[10759])
    drama_shows = Show.objects.filter(genres__contains=[18])
    scifi_shows = Show.objects.filter(genres__contains=[10765])
    comedy_shows = Show.objects.filter(genres__contains=[35])

    context.update({
        'fav_shows': fav_shows,
        'fav_show_ids': fav_show_ids,
        'comp_shows': comp_shows,
        'comp_show_ids': comp_show_ids,
        'watch_shows': watch_shows,
        'watch_show_ids': watch_show_ids,

        'genre_id': genre_id,
        'genre_name': genre_name,
        'crime_shows': crime_shows,
        'action_shows': action_shows,
        'drama_shows': drama_shows,
        'scifi_shows': scifi_shows,
        'comedy_shows': comedy_shows,
    })


    return render(request, "accounts/genre.html", context)

@login_required
def showprofile_view(request, show_id):

    #context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    try:
        # Try to get the Show object first
        show = Show.objects.get(id=show_id)
    except Show.DoesNotExist:
        return HttpResponseNotFound("Show not found")

    context = {'show': show,
               'fav_shows': fav_shows,  # Pass the user's favorited shows to the template
               'fav_show_ids': fav_show_ids,
               'comp_shows': comp_shows,
               'comp_show_ids': comp_show_ids,
               'watch_shows': watch_shows,
               'watch_show_ids': watch_show_ids,

    }

    return render(request, 'accounts/showprofile.html', context)

def will_view(request):
    return render(request, "group/will.html", get_context())