from django.urls import path
from . import views

app_nome = 'agenda'

urlpatterns = [
    path("adicionar/", views.agenda_adicionar, name="agenda_adicionar"),
]