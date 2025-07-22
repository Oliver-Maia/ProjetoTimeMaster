from django.urls import path
from django.urls import include
from . import views

app_name = 'obra'

urlpatterns = [
    path('cadastrar/', views.cadastrar_obra, name='cadastrar_obra'),
    path('editar-excluir/', views.lista_obras, name='editar_excluir_obras'),  # Unificada
    path('listar/', views.lista_obras, name='lista_obras'),  # Mesma view para ambos
    path('api/listar/', views.lista_obras, name='api_listar_obras'),  # Endpoint API
    path('api/obras/<int:obra_id>/', views.editar_obra, name='editar_obra'),
    path('api/obras/<int:obra_id>/excluir/', views.excluir_obra, name='excluir_obra'),
]