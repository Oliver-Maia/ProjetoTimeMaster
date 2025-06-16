from django.urls import path
from . import views

app_nome = 'agenda'

urlpatterns = [
    path("", views.agenda_home),
    path("adicionar/", views.agenda_adicionar)
]