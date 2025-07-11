from django import forms
from agenda.models import Agendamento
from obra.models import obra
from usuario.models import usuario

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['obra', 'data_agendamento', 'montador']  # Somente a obra será selecionada pelo usuário
        widgets = {
            'data_agendamento': forms.DateTimeInput(attrs={'type': 'datetime-local'},
        )}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['obra'].queryset = obra.objects.filter(
            previsao_entrega__isnull=True
        ).exclude(
            agendamentos__isnull=False
        ).distinct()


        self.fields['montador'].queryset = usuario.objects.filter(cargo__nome='Montador', ativo=True).select_related('cargo')
