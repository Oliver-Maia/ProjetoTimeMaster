from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from agenda.models import Agendamento
from .models import Obra

@receiver(post_save, sender=Agendamento)
def atualizar_status_obra(sender, instance, **kwargs):
    if instance.Obra:
        instance.Obra.atualizar_status()

@receiver(post_delete, sender=Agendamento)
def atualizar_status_obra_apos_exclusao(sender, instance, **kwargs):
    if instance.Obra:
        instance.Obra.atualizar_status()