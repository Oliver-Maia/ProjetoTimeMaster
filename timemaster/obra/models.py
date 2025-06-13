from django.db import models

# Create your models here.

class obra(models.Model):
    nome = models.CharField('nome', max_length=50)
    numero_Controle = models.BigIntegerField
    Endereco = models.CharField('endereço', max_length=200, null=True, blank=True)
    data_criacao = models.DateTimeField('Data de criação')
    cliente = models.CharField('nome cliente', max_length=50)
    previsao_entrega = models.DateTimeField('Data prevista para entrega')

    def __str__(self):
        return self.nome