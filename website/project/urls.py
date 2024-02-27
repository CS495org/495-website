"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from our_app.views import RenderAnyTemplate, HomePage
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("", cache_page(60*1)(HomePage.as_view()), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("tv-manager/", include("our_app.urls")),
    path('render-any/<str:to_render>', RenderAnyTemplate.as_view(), name='render-any-view'),
    # path("__debug__/", include("debug_toolbar.urls")),
]