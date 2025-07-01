from usuario.models import Cargo

# Lista de cargos iniciais
cargos_iniciais = ['Montador', 'Administrador']

for nome in cargos_iniciais:
    cargo, criado = Cargo.objects.get_or_create(nome=nome)
    if criado:
        print(f"Cargo criado: {nome}")
    else:
        print(f"Cargo já existia: {nome}")
