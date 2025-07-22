from django.db import models
from obra.models import Obra
from usuario.models import usuario

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    data_agendamento = models.DateTimeField(
        verbose_name='Data de Agendamento',
        null=True,  # Adicionado para permitir agendamentos sem data
        blank=True
    )
    realizado = models.BooleanField(default=False, verbose_name='Agendamento Realizado?')
    cancelado = models.BooleanField(default=False, verbose_name='Agendamento Cancelado?')  # Novo campo
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status do Agendamento'
    )

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_agendamento']
        constraints = [
            models.UniqueConstraint(
                fields=['montador', 'data_agendamento'],
                name='unique_montador_agendamento',
                violation_error_message='Esse montador já tem um agendamento para esse horário.',
                condition=models.Q(data_agendamento__isnull=False)  # Só aplica se tiver data
            )
        ]

    def __str__(self):
        montador_nome = str(self.montador) if self.montador else 'Não designado'
        data_formatada = self.data_agendamento.strftime('%d/%m/%y %H:%M') if self.data_agendamento else 'Sem data'
        return f"{self.obra.nome} - {data_formatada} ({montador_nome}) - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        from_obra = kwargs.pop('from_obra', False)
        self.atualizar_status()
        super().save(*args, **kwargs)

        if not from_obra and hasattr(self, 'obra'):
            if self.obra.status != self.status:
                self.obra.status = self.status
                self.obra.save()
    
    def atualizar_status(self):
        """Atualiza o status baseado nos outros campos"""
        if self.cancelado:
            self.status = 'cancelado'
        elif self.realizado:
            self.status = 'concluido'
        elif self.data_agendamento:
            self.status = 'em_andamento'
        else:
            self.status = 'pendente'

    def marcar_como_concluido(self):
        """Método para marcar como concluído"""
        self.realizado = True
        self.cancelado = False
        self.save()
    
    def marcar_como_cancelado(self):
        """Método para marcar como cancelado"""
        self.cancelado = True
        self.realizado = False
        self.save()


# Signal para garantir que o status seja sempre consistente
@receiver(pre_save, sender=Agendamento)
def atualizar_status_agendamento(sender, instance, **kwargs):
    instance.atualizar_status()
