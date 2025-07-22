from django.db import models
from django.conf import settings

class Obra(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_ANDAMENTO = 'em_andamento'
    STATUS_REALIZADO = 'Realizado'
    STATUS_CANCELADA = 'cancelada'
    STATUS_EXCLUIDA = 'excluida'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_ANDAMENTO, 'Em Andamento'),
        (STATUS_REALIZADO, 'Realizado'),
        (STATUS_CANCELADA, 'Cancelada'),
        (STATUS_EXCLUIDA, 'Excluída'),
    ]

    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    nome = models.CharField('nome', max_length=50)
    numero = models.IntegerField('numero controle')
    endereco = models.TextField('endereço', max_length=200, null=True, blank=True)
    data_criacao = models.DateTimeField('Data de criação', auto_now_add=True)
    cliente = models.CharField('nome cliente', max_length=50)
    previsao_entrega = models.DateTimeField('Data prevista para entrega', null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    excluido = models.BooleanField(default=False)
    usuario_exclusao = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='obras_excluidas'
    )
    data_exclusao = models.DateTimeField(null=True, blank=True)

    def atualizar_status(self):
        """
        Atualiza o status da obra baseado nos agendamentos
        """
        if not hasattr(self, 'agendamentos'):
            return
            
        if self.agendamentos.exists():
            ultimo_agendamento = self.agendamentos.latest('data_agendamento')
            
            if ultimo_agendamento.cancelado:
                self.status = 'cancelado'
            elif ultimo_agendamento.realizado:
                self.status = 'concluido'
            else:
                self.status = 'em_andamento'
        else:
            self.status = 'pendente'
        
        self.save()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['-data_criacao']
    
    @property
    def proximo_agendamento(self):
        return self.agendamentos.filter(realizado=False).order_by('data_agendamento').first()
