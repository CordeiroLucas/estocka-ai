import os
import django
import random

# 1. Configura o ambiente Django para que o script possa acessar o banco
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# 2. Importa os Models (só funciona depois do django.setup())
from estoque.models import Categoria, Produto, Movimentacao
from django.contrib.auth.models import User

def migrate():
    from django.core.management import call_command
    print("\n🔄 Aplicando migrações do banco de dados...\n")
    call_command("migrate", interactive=False)
    print("✅ Migrações aplicadas com sucesso.\n")

def inicializar_usuarios():
    print("\n👤 Verificando usuário Admin...\n")
    if not User.objects.filter(username='admin').exists():
        # Cria o superusuário (usuario, email, senha)
        User.objects.create_superuser('admin', 'admin@exemplo.com', 'admin')
        print("   ✅ Superusuário 'admin' criado com senha 'admin'.")
    else:
        print("   ℹ️ Superusuário 'admin' já existe.")

    print("👤 Verificando usuário Usuário...\n")
    if not User.objects.filter(username='usuario').exists():
        # Cria o usuário comum (usuario, email, senha)
        User.objects.create_user('usuario', 'usuario@exemplo.com', 'usuario')
        print("   ✅ Usuário 'usuario' criado com senha 'usuario'.")
    else:
        print("   ℹ️ Usuário 'usuario' já existe.")

def popular():
    print("\n🚀 Iniciando povoamento do banco de dados...\n")

    # Estrutura de dados solicitada
    dados = {
        "Cookies": [
            "Nestle Cookies",
        ],
        "Cervejas": [
            "Amstel Lager",
            "Budweiser",
        ],
        "Refrigerantes": [
            "Guaraná Zero",
            "Pepsi Zero",
            "Pepsi",
        ],
        "Capsulas": [
            "Capuccino Avela",
            "Cappuccino",
            "Chocolatto",
            "Capuccino Doce de Leite",
            "Chocolatto Caramello",
        ],
        "Salgadinho": [
            "Cebolitos",
            "Doritos",
            "Torcida Churrasco",
            "Torcida Costela c Limao",
        ],
    }

    # login admin senha admin
    # login usuario senha usuario

    for categoria_nome, produtos_lista in dados.items():
        # A. Cria ou Pega a Categoria (evita duplicatas)
        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)

        status_cat = "✅ Criada" if created else "ℹ️ Já existe"
        print(f"{status_cat}: Categoria '{categoria_nome}'")

        # B. Cria os Produtos dessa Categoria
        for produto_nome in produtos_lista:
            # Gera um SKU aleatório para garantir unicidade (Ex: SAL-1234)
            prefixo = categoria_nome[:3].upper()
            sku_gerado = f"{prefixo}-{random.randint(1000, 9999)}"

            # get_or_create verifica pelo nome. Se não existir, usa os 'defaults' para criar.
            produto, prod_created = Produto.objects.get_or_create(
                nome=produto_nome,
                defaults={
                    "categoria": categoria,
                    "preco": 5.00,  # Preço fictício
                    "sku": sku_gerado,
                },
            )

            if prod_created:
                print(f"   └── ➕ Produto criado: {produto_nome} (SKU: {sku_gerado})")
            else:
                # Se o produto já existe, atualizamos a categoria para garantir que está certa
                if produto.categoria != categoria:
                    produto.categoria = categoria
                    produto.save()
                    print(
                        f"   └── 🔄 Atualizado: {produto_nome} movido para {categoria_nome}"
                    )
                else:
                    print(f"   └── ℹ️ Já existe: {produto_nome}")

    print("\n✨ Concluído! O banco de dados foi populado com sucesso.")
    
def popular_movimentos():
    movimentaco = Movimentacao.objects.all()
    if movimentaco.exists():
        print("ℹ️ Movimentações já existem no banco. Pulando povoamento de movimentações.")
        return
    print("\n🚀 Iniciando povoamento de movimentações...\n")

    produtos = list(Produto.objects.all())
    tipos = ['E', 'S']  # Entrada e Saída
    for _ in range(500):  # Cria 500 movimentações
        produto = random.choice(produtos)
        tipo = random.choice(tipos)
        quantidade = random.randint(1, 20)
        observacao = "Movimentação automática para teste."
        destinatario = "Teste Sistema"
        destinatario_cpf = str(random.randint(1,9))*11  # CPF fictício
        try:
            Movimentacao.objects.create(
                produto=produto,
                tipo=tipo,
                quantidade=quantidade,
                usuario=User.objects.get(username='admin') if User.objects.filter(username='admin').exists() else "Teste Sistema",
                solicitante_nome=destinatario,
                solicitante_cpf=destinatario_cpf,
                observacao=observacao,
            )
            print(f"   └── ➕ Movimentação criada: {tipo} de {quantidade} unidades de {produto.nome}")
        except Exception as e:
            print(f"   └── ❌ Erro ao criar movimentação para {produto.nome}: {e}")
    
def build():
    migrate()
    inicializar_usuarios()
    popular()
    popular_movimentos()

if __name__ == "__main__":
    build()
