from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Prefetch
import json
from .forms import ObraForm
from .models import Obra
from agenda.models import Agendamento

@login_required
def cadastrar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            try:
                nova_obra = form.save(commit=False)  # Primeiro não commita
                # Adicione qualquer processamento adicional aqui se necessário
                nova_obra.save()  # Agora salva explicitamente
                
                messages.success(request, f'Obra "{nova_obra.nome}" cadastrada com sucesso!')
               # return redirect('lista_obras')  # Redirecione após POST bem-sucedido
                                
            except Exception as e:
                print(f"Erro ao cadastrar obra: {str(e)}")
                print("Dados do formulário:", request.POST)  # Log dos dados recebidos
                messages.error(request, f'Ocorreu um erro ao cadastrar a obra: {str(e)}')
        else:
            print("Formulário inválido. Erros:", form.errors)  # Log dos erros
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ObraForm()

    return render(request, 'obra/cadastro_obra.html', {'form': form})

from django.db.models import Count
@login_required
def lista_obras(request):
    try:
        status = request.GET.get('status', '')
        excluido = request.GET.get('excluido', 'false') == 'true'
        
        # Query base otimizada
        obras = Obra.objects.all().prefetch_related(
            Prefetch('agendamentos', queryset=Agendamento.objects.order_by('data_agendamento')))
        
        # Filtro de exclusão
        if not excluido:
            obras = obras.filter(excluido=False)
        
        # Filtro por status
        if status:
            if status == 'pendente':
                # Obras pendentes são aquelas SEM agendamentos
                obras = obras.annotate(
                    num_agendamentos=Count('agendamentos')
                ).filter(num_agendamentos=0)
            else:
                obras = obras.filter(status=status)
        
        # Resposta para API
        if request.path.startswith('/obras/api/') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = [{
                'id': ob.id,
                'nome': ob.nome,
                'status': ob.status,
                'tem_agendamento': ob.agendamentos.exists(),
                'data_agendamento': ob.agendamentos.first().data_agendamento.isoformat() 
                    if ob.agendamentos.exists() else None
            } for ob in obras]
            return JsonResponse(data, safe=False)
        
        # Resposta para HTML
        return render(request, 'obra/editar_excluir_obra.html', {
            'obras': obras,
            'status_filter': status
        })
        
    except Exception as e:
        print(f"Erro ao listar obras: {str(e)}")
        if request.path.startswith('/obras/api/'):
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, 'Erro ao carregar a lista de obras')
        return render(request, 'obra/editar_excluir_obra.html', {'obras': []})

@csrf_exempt
@require_http_methods(["PUT"])
@login_required
def editar_obra(request, obra_id):
    try:
        data = json.loads(request.body)
        obra = Obra.objects.get(pk=obra_id)

        obra.nome = data.get('nome', obra.nome)
        obra.numero = data.get('numero', obra.numero)
        obra.cliente = data.get('cliente', obra.cliente)
        obra.endereco = data.get('endereco', obra.endereco)
        obra.status = data.get('status', obra.status)

        obra.save()

        return JsonResponse({'success': True})

    except Obra.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Obra não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@require_http_methods(["DELETE"])
@login_required
def excluir_obra(request, obra_id):
    try:
        obra = Obra.objects.get(pk=obra_id)
        obra.excluido = True
        obra.save()
        return JsonResponse({'success': True})
    except Obra.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Obra não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
