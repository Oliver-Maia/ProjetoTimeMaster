import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timemaster.settings')
django.setup()

# Agora pode importar modelos
from usuario.models import Cargo

cargos_iniciais = ['Montador', 'Administrador']

for nome in cargos_iniciais:
    cargo, criado = Cargo.objects.get_or_create(nome=nome)
    if criado:
        print(f"Cargo criado: {nome}")
    else:
        print(f"Cargo já existia: {nome}")
