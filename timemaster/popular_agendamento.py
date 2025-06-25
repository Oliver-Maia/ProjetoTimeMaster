import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timemaster.settings')
django.setup()

from agenda.models import Agendamento

def criar_agendamento():
    dados_agendamento = [

        {
            'data': datetime.now(),
            'montador' : 'Jhony',
            'realizado': False,
            'obra_id': 2,
            'data_agendamento': '2025-12-21 11:21:10'},

        {
            'data': datetime.now(),
            'montador' : 'Jhony',
            'realizado': False,
            'obra_id': 4,
            'data_agendamento': '2025-09-2 11:21:10'},   
    ]
    
    for dados in dados_agendamento:
        Agendamento.objects.create(**dados)
        print(f"Obra {dados['data']} criada com sucesso!")

if __name__ == '__main__':
    criar_agendamento()