import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timemaster.settings')
django.setup()

from obra.models import obra

def criar_obras():
    dados_obra = [
        {
            'nome': 'Hospital Municipal',
            'numero' : '2522',
            'endereco': 'Av. Saúde, 250',
            'data_criacao': datetime.now(),
            'cliente': 'Prefeitura',
            'previsao_entrega': None },

        {
            'nome': 'Escola Estadual',
            'numero' : '2523',
            'endereco': 'Rua Educação, 100',
            'data_criacao': datetime.now(),
            'cliente': 'Governo do Estado',
            'previsao_entrega': datetime.now() + timedelta(days=60) },

        {
            'nome': 'Shopping Center',
            'numero' : '2524',
            'endereco': 'Av. Comércio, 500',
            'data_criacao': datetime.now(),
            'cliente': 'Grupo Empresarial XYZ',
            'previsao_entrega': None },

        {
            'nome': 'Praça Central',
            'numero' : '2525',
            'endereco': 'Praça da Liberdade, s/n',
            'data_criacao': datetime.now(),
            'cliente': 'Prefeitura Municipal',
            'previsao_entrega': datetime.now() + timedelta(days=15) },    
    ]
    
    for dados in dados_obra:
        obra.objects.create(**dados)
        print(f"Obra {dados['nome']} criada com sucesso!")

if __name__ == '__main__':
    criar_obras()