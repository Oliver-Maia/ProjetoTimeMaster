from django.db import models
from obra.models import Obra
from usuario.models import usuario

class Agendamento(models.Model):
    obra = models.ForeignKey(
        Obra,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name='Obra relacionada'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    montador = models.ForeignKey(
        usuario,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Montador Responsável',
        limit_choices_to={'cargo__nome': 'Montador', 'ativo': True}
    )
    data_agendamento = models.DateTimeField(verbose_name='Data de Agendamento')
    realizado = models.BooleanField(default=False, verbose_name='Agendamento Realizado?')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_agendamento']
        constraints = [
            models.UniqueConstraint(
                fields=['montador', 'data_agendamento'],
                name='unique_montador_agendamento',
                violation_error_message='Esse montador já tem um agendamento para esse horário.'
            )
        ]

    def __str__(self):
        montador_nome = str(self.montador) if self.montador else 'Não designado'
        return f"{self.obra.nome} - {self.data_agendamento.strftime('%d/%m/%y %H:%M')} ({montador_nome})"
