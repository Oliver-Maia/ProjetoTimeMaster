import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timemaster.settings')
django.setup()

from usuario.models import usuario

def criar_usuario():
    dados_usuario = [

        {
            'password': '1212',
            'username' : 'joao',
            'first_name': 'jhony',
            'last_name': 'Aniceto',
            'cpf': '1121106985'},

        {
            'password': '1212',
            'username' : 'Chico',
            'first_name': 'Francisco',
            'last_name': 'Aniceto',
            'cpf': '1121107785'},   
    ]
    
    for dados in dados_usuario:
        usuario.objects.create(**dados)
        print(f"Obra {dados['data']} criada com sucesso!")

if __name__ == '__main__':
    criar_usuario()