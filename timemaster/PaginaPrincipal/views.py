from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from obra.models import obra
from agenda.models import Agendamento
from datetime import datetime, date, timedelta

@login_required
def index(request):
    # Captura da data via GET (vinda do formulário)
    data_str = request.GET.get("data_hoje")

    if data_str:
        try:
            hoje = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            hoje = date.today()
    else:
        hoje = date.today()


    agendamentos_hoje = Agendamento.objects.filter(data=hoje)
    obras_sem_previsao = obra.objects.filter(previsao_entrega__isnull=True)


    semana = [hoje + timedelta(days=i) for i in range(7)]
    agenda_semana = {
        dia: Agendamento.objects.filter(data=dia)
        for dia in semana
    }

    return render(request, 'PaginaPrincipal/paginaprincipal.html', {
        'obras_sem_previsao': obras_sem_previsao,
        'agendamentos_hoje': agendamentos_hoje,
        'agenda_semana': agenda_semana,
        'data_hoje': hoje,  # Enviado de volta para o input[type=date]
    })
