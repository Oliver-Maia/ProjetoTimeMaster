from django.db import models
from obra.models import obra
from usuario.models import usuario
# Create your models here.

class agenda(models.Model):
    obra = models.ForeignKey(obra,on_delete=models.CASCADE)
    entregador = models.ForeignKey(usuario, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField('Data do Agendamento')
    observacoes = models.TextField('Observacoes', null = True, blank = True)
    realizado = models.BooleanField('Realizado', default=False)
    data_realizacao = models.DateTimeField('Data de Realização', null = True, blank = True)

    def __str__(self):
        return self.obra

class Agendamento(models.Model):
    obra = models.ForeignKey(obra, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    montador = models.CharField(max_length=100)  # ou use um FK para um modelo de Funcionário
    data_agendamento = models.DateField()
    realizado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.obra.nome} - {self.data} ({self.montador})"


