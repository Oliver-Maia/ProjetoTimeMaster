from django.shortcuts import render
from .forms import ObraForm
from django.contrib.auth.decorators import login_required
from .models import obra

@login_required
def cadastrar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ObraForm()

    return render(request, 'obra/cadastro_obra.html', {'form': form})


def lista_obras(request):
    obras_pendentes = obra.objects.filter(status='pendente')
    obras_andamento = obra.objects.filter(status='em_andamento')
    obras_concluidas = obra.objects.filter(status='concluida')
    obras_canceladas = obra.objects.filter(status='cancelada')
    
    return render(request, 'lista_obras.html', {
        'obras_pendentes': obras_pendentes,
        'obras_andamento': obras_andamento,
        'obras_canceladas': obras_canceladas,
        'obras_concluidas': obras_concluidas
    })