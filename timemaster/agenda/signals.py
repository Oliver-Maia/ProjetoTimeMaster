from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Obra

@receiver(post_save, sender=Obra)
def sincronizar_status_obra_agendamento(sender, instance, **kwargs):
    # Evita loop infinito
    if kwargs.get('created', False):
        return
    
    for agendamento in instance.agendamentos.all():
        # Atualiza apenas se necessário
        if agendamento.status != instance.status:
            agendamento.status = instance.status
            
            # Atualiza os campos booleanos conforme o status
            if instance.status == 'cancelado':
                agendamento.cancelado = True
                agendamento.realizado = False
            elif instance.status == 'concluido':
                agendamento.realizado = True
                agendamento.cancelado = False
            
            # Salva usando o parâmetro from_obra
            agendamento.save(from_obra=True)