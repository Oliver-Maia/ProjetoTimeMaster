from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.telalogin.as_view(), name ="login"),
    path('agenda/', include(('agenda.urls', 'agenda'), namespace='agenda')),
    path('pagina_inicial/', include('PaginaPrincipal.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='/login/')),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]