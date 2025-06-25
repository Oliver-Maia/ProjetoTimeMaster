from datetime import datetime, timedelta, date
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agenda.models import Agendamento
from obra.models import obra


@login_required
def index(request):
    # 🔹 1. Data selecionada (ou hoje, por padrão)
    data_str = request.GET.get("data_hoje")
    try:
        data_hoje = datetime.strptime(data_str, "%Y-%m-%d").date() if data_str else date.today()
    except ValueError:
        data_hoje = date.today()

    # 🔹 2. Agendamentos do dia (respeitando o cargo)
    if request.user.cargo == 'M':
        agendamentos_hoje = Agendamento.objects.filter(data_agendamento__date=data_hoje, entregador=request.user)
    else:
        agendamentos_hoje = Agendamento.objects.filter(data_agendamento__date=data_hoje)

    # 🔹 3. Obras pendentes
    obras_sem_previsao = obra.objects.filter(previsao_entrega__isnull=True)

    # 🔹 4. Agendamentos da semana (sem incluir hoje)
    inicio = date.today() + timedelta(days=1)
    fim = inicio + timedelta(days=6)

    if request.user.cargo == 'M':
        agendamentos_semana = Agendamento.objects.filter(
            data_agendamento__date__range=(inicio, fim),
            entregador=request.user
        )
    else:
        agendamentos_semana = Agendamento.objects.filter(
            data_agendamento__date__range=(inicio, fim)
        )

    # 🔹 5. Agrupar por data
    agenda_semana = defaultdict(list)
    for ag in agendamentos_semana:
        agenda_semana[ag.data_agendamento.date()].append(ag)

    # 🔹 6. Garantir os dias da semana no dicionário
    semana = [inicio + timedelta(days=i) for i in range(7)]
    agenda_semana_completa = {dia: agenda_semana.get(dia, []) for dia in semana}

    # 🔹 Obras sem previsão
    obras_sem_previsao = obra.objects.filter(
        previsao_entrega__isnull=True)

    # 🔹 Obras com agendamento (não realizado)
    obras_com_agendamento = obra.objects.filter(
        previsao_entrega__isnull=False,
        agendamentos__realizado=False
    ).distinct()

    # 🔹 total de obras que ainda não foram realizadas
    obras_nao_realizadas = obra.objects.exclude(agendamentos__realizado=True).distinct()

    # 🔹 Enviar tudo para o template
    return render(request, 'PaginaPrincipal/paginaprincipal.html', {
        'data_hoje': data_hoje,
        'agendamentos': agendamentos_hoje,
        'obras_sem_previsao': obras_sem_previsao,
        'obras_nao_realizadas': obras_nao_realizadas,
        'obras_com_agendamento': obras_com_agendamento,
        'agenda_semana': agenda_semana_completa,
    })
