from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from agenda.models import Agendamento


@receiver(post_save, sender=Agendamento)
def atualizar_status_obra(sender, instance, **kwargs):
    if instance.obra:
        instance.obra.atualizar_status()
        instance.obra.save()  

@receiver(post_delete, sender=Agendamento)
def atualizar_status_obra_apos_exclusao(sender, instance, **kwargs):
    if instance.obra:
        instance.obra.atualizar_status()
        instance.obra.save()