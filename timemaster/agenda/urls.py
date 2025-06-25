from django.urls import path
from django.urls import include
from . import views


app_name = 'agenda'

urlpatterns = [
    path('adicionar/<int:id>/', views.novo_agendamento, name='agenda_adicionar_com_obra'),
    path('novo/', views.novo_agendamento, name='novo_agendamento'),
    path('', include('PaginaPrincipal.urls')),
]