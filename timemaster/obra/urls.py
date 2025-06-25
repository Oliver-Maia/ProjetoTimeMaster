from django.urls import path
from . import views

app_name = 'obra'

urlpatterns = [
    path('cadastro/', views.cadastrar_obra, name='cadastrar_obra'),
]