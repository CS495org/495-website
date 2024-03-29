"""
URL configuration for cs495_website project.

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
from django.urls import path
from cs495webapp.views import hello_world, RedisView, DatabaseView, RenderAnyTemplate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world, name='hello_world'),
    path('db-test-endpt/', DatabaseView.as_view(), name='db-cbv'),
    path('redis-test-endpt/', RedisView.as_view(), name='redis-cbv'),
    path('render-any/<str:to_render>', RenderAnyTemplate.as_view(), name='render-any-view')
]