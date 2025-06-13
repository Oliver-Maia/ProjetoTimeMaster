from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class usuario(AbstractUser):

    CARGO_CHOICES = [
        ('M', 'Montador'),
        ('A', 'Administrador'),
    ]
    nome = models.CharField('Nome', max_length=200)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    email = models.EmailField('E-mail')
    telefone = models.CharField('Telefone', max_length=20, null=True, blank=True)
    cargo = models.CharField(
        'Cargo',
        max_length=1,
        choices=CARGO_CHOICES  
    )   
    data_admissao = models.DateField('Data de Admissão', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    def __str__(self):
        return self.nome