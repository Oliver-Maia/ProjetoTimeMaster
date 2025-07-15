from django.db import models
from django.conf import settings

class Obra(models.Model):
    status = models.CharField('Status', max_length=20, choices=[
        ('pendente', 'Pendente', ),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada')], default='pendente')
    nome = models.CharField('nome', max_length=50)
    numero = models.IntegerField('numero controle')
    endereco = models.TextField('endereço', max_length=200, null=True, blank=True)
    data_criacao = models.DateTimeField('Data de criação',auto_now_add=True)
    cliente = models.CharField('nome cliente', max_length=50)
    previsao_entrega = models.DateTimeField('Data prevista para entrega', null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    excluido = models.BooleanField(default=False)
    usuario_exclusao = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='obras_excluidas')

    data_exclusao = models.DateTimeField(null=True, blank=True)

    def atualizar_status(self):
        from agenda.models import Agendamento  # Importe aqui para evitar circular imports
        
        if self.excluido:
            self.status = 'excluida'
            self.save()
            return
        
        agendamento = Agendamento.objects.filter(obra=self).first()
        
        if not agendamento:
            self.status = 'pendente'
        elif agendamento.realizado:
            self.status = 'concluida'
        else:
            self.status = 'em_andamento'
        
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