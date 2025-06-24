from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path("adicionar/<int:id>/", views.agenda_adicionar, name="agenda_adicionar"),
    path('hoje/', views.agendamentos_hoje, name='agendamentos_hoje'),
    path('semana/', views.agendamento_semana, name='agendamento_semana'),
]