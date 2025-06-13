from django.shortcuts import render

# Create your views here.


def agenda_home(request):
    return render(request, 'agenda/home.html')

def agenda_adicionar(request):
    return render ()