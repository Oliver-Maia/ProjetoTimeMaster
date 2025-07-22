from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Obra
from agenda.models import Agendamento

@receiver(post_save, sender=Obra)
def sincronizar_status_obra_agendamento(sender, instance, **kwargs):
    # Atualiza todos os agendamentos relacionados à obra
    Agendamento.objects.filter(obra=instance).update(status=instance.status)
    
    # Se precisar de lógica mais complexa:
    for agendamento in instance.agendamentos.all():
        if instance.status == 'cancelado':
            agendamento.cancelado = True
            agendamento.realizado = False
        elif instance.status == 'concluido':
            agendamento.realizado = True
            agendamento.cancelado = False
        agendamento.status = instance.status
        agendamento.save()

@receiver(post_save, sender=Obra)
def sincronizar_status_obra_agendamento(sender, instance, **kwargs):
    for agendamento in instance.agendamentos.all():
        agendamento.status = instance.status
        if instance.status == 'cancelado':
            agendamento.cancelado = True
            agendamento.realizado = False
        elif instance.status == 'concluido':
            agendamento.realizado = True
            agendamento.cancelado = False
        agendamento.save(from_obra=True)