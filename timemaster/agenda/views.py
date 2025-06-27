from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    nome = request.GET.get('nome', '')
    data = request.GET.get('data', '')
    agendamentos = Agendamento.objects.select_related('obra').order_by('data_agendamento')

    if nome:
        agendamentos = agendamentos.filter(obra__nome__icontains=nome)
    
    if data:
        agendamentos = agendamentos.filter(data_agendamento__date=data)

    paginator = Paginator(agendamentos, 3)  # Exibe 10 agendamentos por página
    pagina_num = request.GET.get('page')
    pagina_obj = paginator.get_page(pagina_num)
    
    return render(request, "agenda/listar_agendamentos.html", {
        "pagina_obj": pagina_obj,
        "nome": nome,
        "data": data,
    })
