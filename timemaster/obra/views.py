from django.shortcuts import render
from .forms import ObraForm
from django.contrib.auth.decorators import login_required

@login_required
def cadastrar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ObraForm()

    return render(request, 'obra/cadastro_obra.html', {'form': form})
