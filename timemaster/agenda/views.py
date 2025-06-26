from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from obra.models import obra
from agenda.forms import AgendamentoForm
from agenda.models import Agendamento
from django.utils.timezone import now



@login_required
def novo_agendamento(request, id=None):
    obra_selecionada = None
    if id:
        obra_selecionada = get_object_or_404(obra, id=id)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.data = now()
            agendamento.montador = request.user.get_full_name() or request.user.username
            agendamento.realizado = False
            agendamento.save()
            # Atualiza a previsão de entrega da obra associada ao agendamento
            agendamento.obra.previsao_entrega = agendamento.data_agendamento
            agendamento.obra.save()
    else:
        form = AgendamentoForm(initial={'obra': obra_selecionada})

    return render(request, 'agenda/novo_agendamento.html', {'form': form})

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.select_related('obra').order_by('data_agendamento')

    return render(request, 'agenda/listar_agendamentos.html', {
        'agendamentos': agendamentos
    })
