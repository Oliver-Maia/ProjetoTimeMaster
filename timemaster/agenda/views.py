from django.shortcuts import render, redirect

from obra.models import obra




def agenda_adicionar(request, id):
    obra_obj = obra.objects.get(id=id)
    if request.method == 'POST':
        # Processar o formulário de agendamento aqui
        nova_data = request.POST.get('data_entrega')
        obra_obj.previsao_entrega = nova_data
        obra_obj.save()
        return redirect('obras_pendentes')
    
    return render(request, 'agenda/adicionar.html', {'obra': obra_obj})

