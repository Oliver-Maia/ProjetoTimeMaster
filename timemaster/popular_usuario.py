import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timemaster.settings')
django.setup()

from usuario.models import usuario, Cargo
from django.utils import timezone

def criar_usuario():
    # Buscar ou criar o cargo "Montador"
    cargo_montador, _ = Cargo.objects.get_or_create(nome='Montador')

    dados_usuario = [
        {
            'username': 'joao',
            'first_name': 'Jhony',
            'last_name': 'Aniceto',
            'cpf': '1121106985',
            'email': 'joao@example.com',
            'telefone': '11999999999',
            'cargo': cargo_montador,
        },
        {
            'username': 'chico',
            'first_name': 'Francisco',
            'last_name': 'Aniceto',
            'cpf': '1121107785',
            'email': 'chico@example.com',
            'telefone': '11988888888',
            'cargo': cargo_montador,
        },
    ]

    for dados in dados_usuario:
        if usuario.objects.filter(username=dados['username']).exists():
            print(f"Usuário {dados['username']} já existe. Pulando...")
            continue

        u = usuario(**dados)
        u.set_password('1212')  # Define a senha de forma segura
        u.data_admissao = timezone.now().date()
        u.save()
        print(f"Usuário {u.username} criado com sucesso!")

if __name__ == '__main__':
    criar_usuario()
