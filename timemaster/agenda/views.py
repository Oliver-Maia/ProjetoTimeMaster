from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from obra.models import obra
from agenda.forms import AgendamentoForm
from agenda.models import Agendamento
from django.utils.timezone import now


@login_required
def agenda_adicionar(request, id):
    obra_obj = obra.objects.get(id=id)
    if request.method == 'POST':
        # Processar o formulário de agendamento aqui
        nova_data = request.POST.get('data_entrega')
        obra_obj.previsao_entrega = nova_data
        obra_obj.save()
        return redirect('obras_pendentes')
    
    return render(request, 'agenda/adicionar.html', {'obra': obra_obj})

@login_required
def novo_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.data_agendamento = now()
            agendamento.montador = request.user.get_full_name() or request.user.username
            agendamento.realizado = False
            agendamento.save()
            return redirect('PaginaPrincipal:pagina_inicial')
    else:
        form = AgendamentoForm()

    return render(request, 'agenda/novo_agendamento.html', {'form': form})