from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'PaginaPrincipal'

urlpatterns = [
    path('', views.index, name='pagina_inicial'),
    path('logout/', LogoutView.as_view(), name='logout'),
]