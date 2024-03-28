from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import request, JsonResponse, HttpResponse, HttpRequest
from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.template.exceptions import TemplateDoesNotExist
# from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
# from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.decorators.cache import cache_page
# from our_app.tasks import addfun
from django.views.generic import FormView, UpdateView, RedirectView
# from django.views.generic import UpdateView
from accounts.models import Movie, CustomUser, Show#,# Favorite
from django import forms
from typing import Any
from django.db.utils import IntegrityError

# from .forms import FavMoviesForm
from django.urls import reverse_lazy

from interfaces.objs import pg_interface, red


class HomePage(View):
    template_name = 'home.html'

    def get(self, request: HttpRequest):
        if len(Movie.objects.all()) == 0:
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

        if len(Show.objects.all()) == 0:
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
                    # print(e, row)

        if len(CustomUser.objects.all()) < 2:
            try:
                _new_usr = CustomUser(username='tateb', email='email@email.com',
                                      password=r'pbkdf2_sha256$720000$cRfkFIziOWa16qa9LvYsjy$P2iZiWk50rgncSv/Q3WKM5DTay38UqjxheQiZ5wscy8=')
                _new_usr.save()

            except Exception as e:
                print(e)

        return render(request, self.template_name)#, context=context)


class RedirectToUpdateMovies(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return f"{self.request.user.id}"


class RedirectToUpdateShows(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return f"{self.request.user.id}"


# class

# from django.shortcuts import render, redirect
# from .models import Show, Movie, Favorite

# from django.shortcuts import render
# # from .models import Show, Favorite

def show_list(request):
    shows = Show.objects.all()
    # user = request.user
    # favorites = Favorite.objects.filter(user=user, show__in=shows)
    # favorites_dict = {fav.show_id: fav for fav in favorites}
    return render(request, 'show_list.html', {'shows': shows})


# # Add similar views for movies

# def add_favorite(request, pk):
#     user = request.user
#     show = Show.objects.get(pk=pk)
#     Favorite.objects.create(user=user, show=show)
#     return redirect('show_list')

# # Add similar views for adding favorites for movies

# def update_favorite(request, pk):
#     user = request.user
#     show = Show.objects.get(pk=pk)
#     favorite = Favorite.objects.get(user=user, show=show)

#     if request.method == 'POST':
#         # Handle form submission to update favorite
#         # Example: favorite.rating = request.POST['rating']
#         favorite.save()
#         return redirect('show_list')

#     return render(request, 'update_shows.html', {'favorite': favorite})

# # Add similar views for updating favorites for movies

# def delete_favorite(request, pk):
#     user = request.user
#     show = Show.objects.get(pk=pk)
#     favorite = Favorite.objects.get(user=user, show=show)
#     favorite.delete()
#     return redirect('show_list')

# Add similar views for deleting favorites for movies


class UpdateFavMoviesView(LoginRequiredMixin, UpdateView):
    template_name = 'update_movies.html'
    # form_class = FavMoviesForm
    success_url = reverse_lazy('home')
    model = CustomUser

    fields = ['fav_movies']
    _movie = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    queryset = CustomUser.objects.all()

# class AllMovieView(generic.ListView)


class UpdateFavShowsView(LoginRequiredMixin, UpdateView):
    template_name = 'update_shows.html'
    # form_class = FavMoviesForm
    success_url = reverse_lazy('home')
    model = CustomUser

    fields = ['fav_shows']
    _show = forms.ModelMultipleChoiceField(
        queryset=Show.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    queryset = CustomUser.objects.all()



# from django.views.generic.detail import DetailView

# class PersonDetailView(DetailView):
#     template_name = "update_shows.html"
#     model = CustomUser

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         person = get_object_or_404(CustomUser,pk=self.kwargs['pk'])
#         context['meetings_today'] = person.meetings_today()
#         context['tasks_due_today'] = person.tasks_due_today()
#         return context


class RenderAnyTemplate(View):
    '''class for quickly developing frontend features\n
    will attempt to render html template found at dev_templates/<file_name>.html\n
    to use this: drop your html template in ./templates/dev_templates, then
    go to https://localhost/render-any/<FILE_NAME>\n
    don't include the .html file extension'''

    def get(self, request: HttpRequest, to_render: str) -> HttpResponse:
            file_path = 'render_any/' + to_render + '.html'

            return render(request, file_path)


class RedisView(View):
    '''redis class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''increment page hits, return it as json'''
        try:
            page_hits = red.incr('page_hits')
            return JsonResponse(data = {"response" : f"Page hits: {page_hits}"})

        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})


# class DatabaseView(LoginRequiredMixin, View):
class DatabaseView(View):
    '''database class based view'''

    def get(self, request: HttpRequest) -> JsonResponse:
        '''get * from public.example_table'''
        try:
            rows = pg_interface.get_rows(table_name='"Top_Rated_Movies"')
            return JsonResponse(data = {"response" : rows})

        except Exception as e:
            return JsonResponse(data = {"error" : str(e)})