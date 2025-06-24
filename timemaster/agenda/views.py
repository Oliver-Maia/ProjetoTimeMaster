from django.shortcuts import render, redirect
from django.utils.timezone import now
from obra.models import obra
from .models import Agendamento
from datetime import date, timedelta
from collections import defaultdict


# View para listar obras pendentes

def agenda_adicionar(request, id):
    obra_obj = obra.objects.get(id=id)
    if request.method == 'POST':
        # Processar o formulário de agendamento aqui
        nova_data = request.POST.get('data_entrega')
        obra_obj.previsao_entrega = nova_data
        obra_obj.save()
        return redirect('obras_pendentes')
    
    return render(request, 'agenda/adicionar.html', {'obra': obra_obj})


def agendamentos_hoje(request):
    hoje = date.today()
    if request.user.cargo == 'M':  # Montador
        agendamentos = Agendamento.objects.filter(data_agendamento=hoje, entregador=request.user)
    else:  # Administrador
        agendamentos = Agendamento.objects.filter(data_agendamento=hoje)

    return render(request, 'agenda/agendamentos_hoje.html', {'agendamentos': agendamentos})



def agendamento_semana(request):
    hoje = now().date()
    fim_periodo = timedelta(days=7)

    if request.user.cargo == 'M':  # Montador
        agendamentos = Agendamento.objects.filter(data_agendamento__range=(hoje, fim_periodo), entregador=request.user)
    else:  # Administrador
        agendamentos = Agendamento.objects.filter(data_agendamento__range=(hoje, fim_periodo))

    # Agrupar por dia
    agenda_semana = defaultdict(list)
    for agendamento in agendamentos:
        agenda_semana[agendamento.data_agendamento].append(agendamento)

    # Ordenar por dia
    agenda_semana = dict(sorted(agenda_semana.items()))

    return render(request, 'agenda/agendamento_semana.html', {
        'agenda_semana': agenda_semana
    })