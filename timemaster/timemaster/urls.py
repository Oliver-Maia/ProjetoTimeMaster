from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("agenda/", include("agenda.urls")),
    path("__reload__/", include("django_browser_reload.urls"))
]
