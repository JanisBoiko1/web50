from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage"),
   
]
