from django.db import models

# Create your models here.

class obra(models.Model):
    nome = models.CharField('nome', max_length=50)
    numero = models.IntegerField('numero controle')
    endereco = models.TextField('endereço', max_length=200, null=True, blank=True)
    data_criacao = models.DateTimeField('Data de criação',auto_now_add=True)
    cliente = models.CharField('nome cliente', max_length=50)
    previsao_entrega = models.DateTimeField('Data prevista para entrega', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.numero}"