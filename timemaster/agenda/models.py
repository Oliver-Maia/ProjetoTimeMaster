from django.conf import settings
from django.db import models
from obra.models import Obra
from usuario.models import usuario
# Create your models here.

class agenda(models.Model):
    obra = models.ForeignKey(Obra,on_delete=models.CASCADE, related_name='agendamentos_secundario')
    entregador = models.ForeignKey(usuario, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField('Data do Agendamento')
    observacoes = models.TextField('Observacoes', null = True, blank = True)
    realizado = models.BooleanField('Realizado', default=False)
    data_realizacao = models.DateTimeField('Data de Realização', null = True, blank = True)

    def __str__(self):
        return self.obra

class Agendamento(models.Model):
    obra = models.ForeignKey('Obra.Obra', on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Obra relacionada')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    montador = models.ForeignKey('usuario.Usuario', on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Montador Responsável', limit_choices_to={'cargo__nome' :'Montador', 'ativo': True})
    data_agendamento = models.DateTimeField(verbose_name='Data de Agendamento')
    realizado = models.BooleanField(default=False, verbose_name='Agendamento Realizado?')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_agendamento']
        constraints = [
            models.UniqueConstraint(fields=['montador', 'data_agendamento'], name='unique_montador_agendamento',
                violation_error_message='Esse montador ja tem um agendamento para esse horario.')
        ]

    def __str__(self):
        montador_nome = str(self.montador) if self.montador else 'Não designado'
        return f"{self.obra.nome} - {self.data_agendamento.strftime('$d/%m/%y %H:%M')} ({montador_nome})"

    
