from django import forms
from agenda.models import Agendamento
from obra.models import obra

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['obra', 'data_agendamento']  # Somente a obra será selecionada pelo usuário

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lista apenas obras que ainda não têm agendamento ou não estão finalizadas
        self.fields['obra'].queryset = obra.objects.filter(
            previsao_entrega__isnull=True,
            agendamentos__realizado=False
        ).distinct()
