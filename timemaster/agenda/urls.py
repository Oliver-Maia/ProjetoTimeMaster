from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path("adicionar/<int:id>/", views.agenda_adicionar, name="agenda_adicionar"),
]