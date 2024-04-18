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

        fav_top_rated = request.user.fav_top_rated.all()
        fav_top_ids = set(fav_top_rated.values_list('id', flat=True))

        comp_shows = request.user.comp_shows.all()
        comp_show_ids = set(comp_shows.values_list('id', flat=True))

        comp_top_rated = request.user.comp_top_rated.all()
        comp_top_ids = set(comp_top_rated.values_list('id', flat=True))

        watch_shows = request.user.watch_shows.all()
        watch_show_ids = set(watch_shows.values_list('id', flat=True))

        watch_top_rated = request.user.watch_top_rated.all()
        watch_top_ids = set(watch_top_rated.values_list('id', flat=True))

        context.update({
            'fav_shows': fav_shows,
            'fav_show_ids': fav_show_ids,
            'fav_top_rated': fav_top_rated,
            'fav_top_ids': fav_top_ids,
            'comp_shows': comp_shows,
            'comp_show_ids': comp_show_ids,
            'comp_top_rated': comp_top_rated,
            'comp_top_ids': comp_top_ids,
            'watch_shows': watch_shows,
            'watch_show_ids': watch_show_ids,
            'watch_top_rated': watch_top_rated,
            'watch_top_ids': watch_top_ids,

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


class AjaxUpdateFavTopView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                
                #handle fav_top_rated list
                top = TopRatedShow.objects.get(pk=show_id)
                if user.fav_top_rated.filter(pk=show_id).exists():
                    user.fav_top_rated.remove(top)
                    action_fav_top = 'removed'
                else:
                    user.fav_top_rated.add(top)
                    action_fav_top = 'added'
                
                user.save()

                fav_top_ids = list(user.fav_top_rated.values_list('id', flat=True))
                
                return JsonResponse({'action_fav_top': action_fav_top, 'fav_top_ids': fav_top_ids})
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


class AjaxUpdateCompTopView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                
                #handle fav_top_rated list
                top = TopRatedShow.objects.get(pk=show_id)
                if user.comp_top_rated.filter(pk=show_id).exists():
                    user.comp_top_rated.remove(top)
                    action_comp_top = 'removed'
                else:
                    user.comp_top_rated.add(top)
                    action_comp_top = 'added'
                
                user.save()

                comp_top_ids = list(user.comp_top_rated.values_list('id', flat=True))
                
                return JsonResponse({'action_comp_top': action_comp_top, 'comp_top_ids': comp_top_ids})
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


class AjaxUpdateWatchTopView(LoginRequiredMixin, UpdateView):
    #success_url = reverse_lazy('home')
    model = CustomUser

    def post(self, request, *args, **kwargs):
        show_id = kwargs.get('show_id')
        if show_id:
            try:
                user = self.request.user
                
                #handle fav_top_rated list
                top = TopRatedShow.objects.get(pk=show_id)
                if user.comp_top_rated.filter(pk=show_id).exists():
                    user.watch_top_rated.remove(top)
                    action_watch_top = 'removed'
                else:
                    user.watch_top_rated.add(top)
                    action_watch_top = 'added'
                
                user.save()

                watch_top_ids = list(user.watch_top_rated.values_list('id', flat=True))
                
                return JsonResponse({'action_watch_top': action_watch_top, 'watch_top_ids': watch_top_ids})
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

    fav_top_rated = request.user.fav_top_rated.all()
    fav_top_ids = set(fav_top_rated.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    comp_top_rated = request.user.comp_top_rated.all()
    comp_top_ids = set(comp_top_rated.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    watch_top_rated = request.user.watch_top_rated.all()
    watch_top_ids = set(watch_top_rated.values_list('id', flat=True))

    context.update({
        'fav_shows': fav_shows,
        'fav_show_ids': fav_show_ids,
        'fav_top_rated': fav_top_rated,
        'fav_top_ids': fav_top_ids,
        'comp_shows': comp_shows,
        'comp_show_ids': comp_show_ids,
        'comp_top_rated': comp_top_rated,
        'comp_top_ids': comp_top_ids,
        'watch_shows': watch_shows,
        'watch_top_ids': watch_top_ids
    })

    return render(request, "accounts/profile.html", context)

def calendar_view(request):
    return render(request, "accounts/calendar.html", get_context())

def discover_view(request):
    context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    fav_top_rated = request.user.fav_top_rated.all()
    fav_top_ids = set(fav_top_rated.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    comp_top_rated = request.user.comp_top_rated.all()
    comp_top_ids = set(comp_top_rated.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    watch_top_rated = request.user.watch_top_rated.all()
    watch_top_ids = set(watch_top_rated.values_list('id', flat=True))

    context.update({
        'fav_shows': fav_shows,
        'fav_show_ids': fav_show_ids,
        'fav_top_rated': fav_top_rated,
        'fav_top_ids': fav_top_ids,
        'comp_shows': comp_shows,
        'comp_show_ids': comp_show_ids,
        'comp_top_rated': comp_top_rated,
        'comp_top_ids': comp_top_ids,
        'watch_shows': watch_shows,
        'watch_top_ids': watch_top_ids
    })

    return render(request, "accounts/discover.html", context)

def settings_view(request):
    return render(request, "accounts/settings.html", get_context())

def group_view(request):
    return render(request, "accounts/group.html", get_context())

def genre_view(request):
    context = get_context()
    context["image_files"] = [f"{i}.jpg" for i in range(51)]
    return render(request, "accounts/genre.html", context)

def showprofile_view(request, show_id):

    #context = get_context()

    fav_shows = request.user.fav_shows.all()
    fav_show_ids = set(fav_shows.values_list('id', flat=True))

    fav_top_rated = request.user.fav_top_rated.all()
    fav_top_ids = set(fav_top_rated.values_list('id', flat=True))

    comp_shows = request.user.comp_shows.all()
    comp_show_ids = set(comp_shows.values_list('id', flat=True))

    comp_top_rated = request.user.comp_top_rated.all()
    comp_top_ids = set(comp_top_rated.values_list('id', flat=True))

    watch_shows = request.user.watch_shows.all()
    watch_show_ids = set(watch_shows.values_list('id', flat=True))

    watch_top_rated = request.user.watch_top_rated.all()
    watch_top_ids = set(watch_top_rated.values_list('id', flat=True))

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
    
    context = {'show': show,
               'fav_shows': fav_shows,  # Pass the user's favorited shows to the template
               'fav_show_ids': fav_show_ids,
               'fav_top_rated': fav_top_rated,
               'fav_top_ids': fav_top_ids,
               'comp_shows': comp_shows,
               'comp_show_ids': comp_show_ids,
               'comp_top_rated': comp_top_rated,
               'comp_top_ids': comp_top_ids,
               'watch_shows': watch_shows,
               'watch_show_ids': watch_show_ids,
               'watch_top_rated': watch_top_rated,
               'watch_top_ids': watch_top_ids

    }
    
    return render(request, 'accounts/showprofile.html', context)

def will_view(request):
    return render(request, "group/will.html", get_context())