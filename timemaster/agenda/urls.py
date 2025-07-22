from django.urls import path
from django.urls import include
from . import views


app_name = 'agenda'

urlpatterns = [
    path('adicionar/<int:id>/', views.novo_agendamento, name='agenda_adicionar_com_obra'),
    path('novo/', views.novo_agendamento, name='novo_agendamento'),
    path('lista/', views.listar_agendamentos, name='listar'),
    path('agenda/', views.listar_agendamentos, name='agenda'),
    path('agendamento/<int:agendamento_id>/status/<str:novo_status>/', views.atualizar_status, name='atualizar_status'),
    path('eventos/', views.eventos_json, name='eventos_json'),
    path('calendario/', views.tela_agenda, name='calendario'),
    path('', include('PaginaPrincipal.urls')),
]