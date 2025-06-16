from django.shortcuts import render
from django.contrib.auth.views import LoginView


class telalogin(LoginView):
    template_name = 'login.html'