from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from obra.models import Obra
from agenda.forms import AgendamentoForm
from agenda.models import Agendamento


@login_required
def novo_agendamento(request, id=None):
    obra_selecionada = None
    if id:
        obra_selecionada = get_object_or_404(Obra, id=id)

    # Processar formulário se for POST
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            agendamento = form.save(commit=False)
            

            if agendamento.obra.status != 'pendente':
                messages.error(request, 'Só é permitido agendar obras com status "Pendente".')
                return redirect('agenda:agenda_adicionar_com_obra', id=agendamento.obra.id)

            agendamento.data_criacao = now()
            agendamento.realizado = False
            agendamento.save()
            
            # Atualizar o status da obra após agendar
            if agendamento.obra:
                agendamento.obra.previsao_entrega = agendamento.data_agendamento
                agendamento.obra.status = 'em_andamento'
                agendamento.obra.save()
            
            messages.success(request, 'Agendamento criado com sucesso!')
            
            # Após salvar, redirecionar para a URL, não para um template
            return redirect('agenda:novo_agendamento')

        else: # Se o formulário não for válido, exibe os erros e o formulário preenchido
            messages.error(request, 'O formulário contém erros. Verifique os campos.')
            
            # Neste caso, renderizamos o template com o formulário e os erros.
            agendamentos = Agendamento.objects.all().order_by('-data_criacao')[:5]
            obras_filtradas = Obra.objects.filter(status='pendente')

            return render(request, 'agenda/novo_agendamento.html', {
                'form': form,
                'agendamentos': agendamentos,
                'obras_pendentes': obras_filtradas,
                'obra_selecionada': obra_selecionada
            })


    else:  # Lógica para requisições GET
        initial = {'obra': obra_selecionada} if obra_selecionada else {}
        form = AgendamentoForm(initial=initial)

    # Lógica de renderização para requisições GET
    agendamentos = Agendamento.objects.all().order_by('-data_criacao')[:5]
    status_filter = request.GET.get('status')
    if status_filter:
        obras_filtradas = Obra.objects.filter(status=status_filter)
    else:
        obras_filtradas = Obra.objects.filter(status='pendente')

    template_name = 'agenda/novo_agendamento.html' if not request.GET.get('modal') else 'agenda/formAgendamento.html'
    
    return render(request, template_name, {
        'form': form,
        'agendamentos': agendamentos,
        'obras_pendentes': obras_filtradas,
        'obra_selecionada': obra_selecionada,
        'status_filter': status_filter
    })

from django.shortcuts import redirect

@login_required
def listar_agendamentos(request):
    nome = request.GET.get('nome', '')
    data = request.GET.get('data', '')
    status_filtro = request.GET.get('status', '')

    # Filtrar apenas agendamentos existentes, com joins
    agendamentos = Agendamento.objects.select_related('obra', 'montador').filter(obra__excluido=False)

    # Filtros
    if nome:
        agendamentos = agendamentos.filter(obra__nome__icontains=nome)
    if data:
        agendamentos = agendamentos.filter(data_agendamento__date=data)
    if status_filtro:
        agendamentos = agendamentos.filter(obra__status=status_filtro)

    agendamentos = agendamentos.order_by('-data_agendamento')

    # Paginação
    paginator = Paginator(agendamentos, 10)  # 10 por página
    page_number = request.GET.get('page')
    pagina_obj = paginator.get_page(page_number)

    context = {
        'pagina_obj': pagina_obj,
        'nome': nome,
        'data': data,
        'status_filtro': status_filtro,
    }
    return render(request, 'agenda/listar_agendamentos.html', context)

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
        event_dict = {
            'title': f'{evento.obra.nome} - {evento.montador}',
            'start': evento.data_agendamento.isoformat(),
            'color': cores.get(evento.montador, '#7f8c8d'),
        }

        if evento.data_agendamento.hour == 0 and \
           evento.data_agendamento.minute == 0 and \
           evento.data_agendamento.second == 0:
            event_dict['allDay'] = True
            # Se for 00:00:00, define o final como o dia seguinte
            event_dict['end'] = (evento.data_agendamento + timedelta(days=1)).isoformat()
        else:
            # Se não for 00:00:00, use seu cálculo de duração padrão
            event_dict['end'] = (evento.data_agendamento + timedelta(hours=2)).isoformat()

        data.append(event_dict)

    return JsonResponse(data, safe=False)

@login_required
def atualizar_status(request, agendamento_id, novo_status):
    if request.method == 'POST':
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        if novo_status == 'concluido':
            agendamento.realizado = True
            agendamento.cancelado = False
        elif novo_status == 'cancelado':
            agendamento.cancelado = True
            agendamento.realizado = False
        
        agendamento.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'status': agendamento.get_status_display(),
                'status_class': agendamento.status
            })
        return redirect('listar_agendamentos')
    
    return JsonResponse({'success': False}, status=400)

@login_required
def tela_agenda(request):
    return render(request, 'agenda/telaAgenda.html')