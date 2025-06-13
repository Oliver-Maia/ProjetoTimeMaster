from django.urls import path
from . import views

urlpatterns = [
    path("", views.agenda_home),
    path("adicionar/", views.agenda_adicionar)
]