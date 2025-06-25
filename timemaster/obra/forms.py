from django import forms
from .models import obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = obra
        fields = ['nome', 'numero', 'endereco', 'cliente', 'previsao_entrega']  
        widgets = {
            'previsao_entrega': forms.DateInput(attrs={'type': 'date'}),
        }
    labels = {
        'nome': 'Nome da Obra',
        'numero': 'Número da Obra',
        'endereco': 'Endereço da Obra',
        'cliente': 'Cliente',
        'previsao_entrega': 'Previsão de Entrega', }
