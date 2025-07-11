from django import forms
from .models import obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = obra
        fields = ['nome', 'numero', 'endereco', 'cliente',]  
        
    labels = {
        'nome': 'Nome da Obra',
        'numero': 'Número da Obra',
        'endereco': 'Endereço da Obra',
        'cliente': 'Cliente',
        }
