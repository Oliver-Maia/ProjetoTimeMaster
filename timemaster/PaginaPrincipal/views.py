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

    # 🔹 3. Obras por status (novo)
    obras_pendentes = obra.objects.filter(status='pendente')
    obras_andamento = obra.objects.filter(status='em_andamento')
    obras_concluidas = obra.objects.filter(status='concluida')
    obras_canceladas = obra.objects.filter(status='cancelada')

    # 🔹 4. Timeline dos próximos 5 dias (ao invés da semana toda)
    timeline = {}
    for i in range(5):
        dia = data_hoje + timedelta(days=i)
        if request.user.cargo == 'M':
            agendamentos = Agendamento.objects.filter(
                data_agendamento__date=dia,
                entregador=request.user
            ).order_by('data_agendamento')
        else:
            agendamentos = Agendamento.objects.filter(
                data_agendamento__date=dia
            ).order_by('data_agendamento')
        timeline[dia] = agendamentos

    # 🔹 5. Estatísticas para os cards (atualizadas)
    total_obras_aberto = obras_pendentes.count() + obras_andamento.count()
    
    # 🔹 6. Obras sem previsão (para o carrossel)
    obras_sem_previsao = obra.objects.filter(
        previsao_entrega__isnull=True,
        status='pendente'  # Apenas obras pendentes
    )

    return render(request, 'PaginaPrincipal/paginaprincipal.html', {
        'data_hoje': data_hoje,
        'agendamentos': agendamentos_hoje,
        
        # Novos contextos para status
        'obras_pendentes': obras_pendentes,
        'obras_andamento': obras_andamento,
        'obras_concluidas': obras_concluidas,
        'obras_canceladas': obras_canceladas,
        
        # Timeline dos próximos 5 dias
        'timeline': timeline,
        
        # Estatísticas para os cards
        'total_obras_aberto': total_obras_aberto,
        
        # Mantendo compatibilidade com o template antigo
        'obras_sem_previsao': obras_sem_previsao,
        'obras_com_agendamento': obras_andamento,  # Agora usa obras em andamento
        'agenda_semana': timeline,  # Mantém o nome antigo para compatibilidade
    })