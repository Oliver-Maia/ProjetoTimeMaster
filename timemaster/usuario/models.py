from django.contrib.auth.models import AbstractUser
from django.db import models

class Cargo(models.Model):
    nome = models.CharField('Nome do Cargo', max_length=100, unique=True)

    def __str__(self):
        return self.nome

class usuario(AbstractUser):
    nome = models.CharField('Nome', max_length=200)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    email = models.EmailField('E-mail')
    telefone = models.CharField('Telefone', max_length=20, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, verbose_name='Cargo', on_delete=models.SET_NULL, null=True)
    data_admissao = models.DateField('Data de Admissão', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    def __str__(self):
        name = self.get_full_name()
        if name and name.strip():
            return name.strip()
        return self.username or f"Usuário #{self.id}"

