from django.urls import path
from .views import lista_obras_pendentes

urlpatterns = [
    path("", lista_obras_pendentes, name='obras_pendentes'),
]