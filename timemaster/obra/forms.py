from django import forms
from .models import Obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nome', 'numero', 'endereco', 'cliente',]  
        
    labels = {
        'nome': 'Nome da Obra',
        'numero': 'Número da Obra',
        'endereco': 'Endereço da Obra',
        'cliente': 'Cliente',
        }
