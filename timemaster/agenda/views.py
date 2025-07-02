from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.core.paginator import Paginator
from obra.models import obra
from agenda.forms import AgendamentoForm
from agenda.models import Agendamento
from django.utils.timezone import now
from django.http import JsonResponse



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
            agendamento.montador = request.POST.get('montador', None)
            agendamento.realizado = False
            agendamento.save()
            agendamento.obra.previsao_entrega = agendamento.data_agendamento
            agendamento.obra.save()
    else:
        form = AgendamentoForm(initial={'obra': obra_selecionada})
    if request.GET.get('modal') == '1':
        template_name = 'agenda/formAgendamento.html'
    else:
        template_name = 'agenda/novo_agendamento.html'

    return render(request, template_name, {'form': form})

@login_required
def listar_agendamentos(request):
    nome = request.GET.get('nome', '')
    data = request.GET.get('data', '')
    agendamentos = Agendamento.objects.select_related('obra').order_by('data_agendamento')
    montador_nome = request.GET.get('montador', '')

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
        'montador': montador_nome,
    })

@login_required
def eventos_json(request):
    eventos = Agendamento.objects.select_related('obra').all()

    cores = {
        'Montador A': '#1abc9c',
        'Montador B': '#3498db',
        'Montador C': '#e67e22',
    }

    data = []
    for evento in eventos:
        data.append({
            'title': f'{evento.obra.nome} - {evento.montador}',
            'start': evento.data_agendamento.isoformat(),
            'end': (evento.data_agendamento + timedelta(hours=2)).isoformat(),
            'color': cores.get(evento.montador, '#7f8c8d'),
        })

    return JsonResponse(data, safe=False)

@login_required
def tela_agenda(request):
    return render(request, 'agenda/telaAgenda.html')