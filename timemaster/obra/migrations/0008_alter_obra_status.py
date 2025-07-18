# Generated by Django 5.0.14 on 2025-07-18 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obra', '0007_alter_obra_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('em_andamento', 'Em Andamento'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada'), ('excluida', 'Excluída')], default='pendente', max_length=20, verbose_name='Status'),
        ),
    ]
