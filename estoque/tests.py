from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Categoria, Produto, Movimentacao

class EstoqueModelTests(TestCase):
    """
    TESTES UNITÁRIOS: Focam na lógica pura dos Models (Banco de Dados).
    Testam se as contas batem e se as regras de validação funcionam.
    """

    def setUp(self):
        # Cria dados iniciais para usar nos testes
        self.user = User.objects.create_user(username='tester', password='123')
        self.categoria = Categoria.objects.create(nome="Eletronicos")
        self.produto = Produto.objects.create(
            nome="Mouse", 
            categoria=self.categoria, 
            quantidade=0 # Começa zerado
        )

    def test_geracao_sku_automatica(self):
        """Testa se o SKU é gerado automaticamente baseado na categoria"""
        self.assertTrue(self.produto.sku.startswith("ELE-"))
        print(f"✅ SKU Gerado: {self.produto.sku}")

    def test_entrada_estoque(self):
        """Testa se uma entrada aumenta a quantidade do produto"""
        Movimentacao.objects.create(
            usuario=self.user,
            tipo='E',
            produto=self.produto,
            quantidade=10
        )
        # Recarrega do banco para ver o valor atualizado
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 10)
        print(f"✅ Quantidade após entrada (10): {self.produto.quantidade}")

    def test_saida_estoque(self):
        """Testa se uma saída diminui a quantidade"""
        # 1. Dá uma entrada de 20
        Movimentacao.objects.create(usuario=self.user, tipo='E', produto=self.produto, quantidade=20)
        
        # 2. Faz uma saída de 5
        Movimentacao.objects.create(usuario=self.user, tipo='S', produto=self.produto, quantidade=5)
        
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 15)
        print(f"✅ Quantidade após saída (20-5): {self.produto.quantidade}")

    def test_bloqueio_estoque_negativo(self):
        """Testa se o sistema impede saída maior que o saldo"""
        # Saldo é 0. Tentar tirar 1 deve falhar.
        mov = Movimentacao(
            usuario=self.user,
            tipo='S',
            produto=self.produto,
            quantidade=1
        )
        
        # Espera que levante um ValidationError ao chamar clean() ou save()
        with self.assertRaises(ValidationError):
            mov.save()
        print("✅ Bloqueio de estoque negativo funcionou corretamente.")

    # def test_limite_cpf_diario(self):
    #     """Testa a regra de ouro: Máximo 3 retiradas por CPF por dia"""
    #     # Dá saldo suficiente primeiro
    #     Movimentacao.objects.create(usuario=self.user, tipo='E', produto=self.produto, quantidade=100)
        
    #     cpf_teste = "123.456.789-00"

    #     # Faz 3 retiradas (Deve permitir)
    #     for i in range(3):
    #         Movimentacao.objects.create(
    #             usuario=self.user,
    #             tipo='S',
    #             produto=self.produto,
    #             quantidade=1,
    #             solicitante_cpf=cpf_teste
    #         )

    #     # Tenta a 4ª retirada (Deve bloquear)
    #     mov_bloqueada = Movimentacao(
    #         usuario=self.user,
    #         tipo='S',
    #         produto=self.produto,
    #         quantidade=1,
    #         solicitante_cpf=cpf_teste
    #     )

    #     with self.assertRaisesRegex(ValidationError, "limite de 3 retiradas"):
    #         mov_bloqueada.clean()


class EstoqueViewTests(TestCase):
    """
    TESTES DE INTEGRAÇÃO: Focam no fluxo (URLs, Views, Permissões).
    Testam se o usuário consegue ver o que deveria ver.
    """

    def setUp(self):
        # Usuário Comum
        self.user_comum = User.objects.create_user(username='comum', password='123')
        # Admin (Superusuário)
        self.admin = User.objects.create_superuser(username='admin', password='123')
        
        self.categoria = Categoria.objects.create(nome="Geral")
        self.produto = Produto.objects.create(nome="Caneta", categoria=self.categoria)

    def test_redirecionamento_usuario_comum(self):
        """Usuário comum tentando acessar dashboard deve ir para a Saída Rápida"""
        self.client.login(username='comum', password='123')
        
        response = self.client.get(reverse('dashboard'))
        
        # Código 302 = Redirecionamento
        self.assertEqual(response.status_code, 302)
        # Verifica se foi para a URL correta
        self.assertIn(reverse('registrar_saida_rapida'), response.url)
        print("✅ Usuário comum foi redirecionado corretamente para Saída Rápida.")

    def test_acesso_admin_dashboard(self):
        """Admin deve conseguir acessar o dashboard (status 200)"""
        self.client.login(username='admin', password='123')
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estoque Atual")
        print("✅ Admin acessou o dashboard com sucesso.")

    def test_registro_movimentacao_view(self):
        """Testa o fluxo completo de enviar o formulário via POST"""
        self.client.login(username='admin', password='123')
        
        # Dados do formulário
        dados = {
            'tipo': 'E', # Entrada
            'categoria': self.categoria.id,
            'produto': self.produto.id,
            'quantidade': 50,
            'solicitante_nome': 'Teste View'
        }

        # Simula o POST
        url = reverse('registrar_saida_rapida')
        response = self.client.post(url, dados)

        # Deve redirecionar após sucesso (302)
        self.assertEqual(response.status_code, 302)

        # Verifica se gravou no banco
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 50)
        print(f"✅ Movimentação registrada via view. Nova quantidade: {self.produto.quantidade}")