from obra.models import obra
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_obras_pendentes(request):
    obras_sem_previsao = obra.objects.filter(previsao_entrega__isnull=True)
    return render(request, 'obra/obras_pendentes.html', {'obras_sem_previsao': obras_sem_previsao})
