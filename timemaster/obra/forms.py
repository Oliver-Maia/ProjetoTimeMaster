from django import forms
from .models import obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = obra
        fields = ['nome', 'numero', 'endereco', 'cliente','status',]  
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
    labels = {
        'nome': 'Nome da Obra',
        'numero': 'Número da Obra',
        'endereco': 'Endereço da Obra',
        'cliente': 'Cliente',
        'status': 'Status da Obra',
        }
