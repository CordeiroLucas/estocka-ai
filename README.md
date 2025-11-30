# 📦 Estocka-Ai - Sistema de Controle de Estoque v1.7

Um sistema de gerenciamento de estoque escalável, seguro e moderno, desenvolvido com **Django**. O projeto utiliza uma arquitetura robusta com validações de integridade, interface **Mobile-First** para operações rápidas e está totalmente configurado para deploy na **Vercel** com banco de dados hospedado no Neon.tech utilizando **PostgreSQL**.

---

## 🚀 Funcionalidades

### 🔹 Gestão e Controle
* **Dashboard Inteligente:** Visão geral com paginação, filtros por Categoria/Nome/SKU e alertas visuais de estoque baixo.
* **Sincronização de Saldo:** Botão exclusivo para administradores que recalcula o saldo de todos os produtos com base no histórico de movimentações (Ferramenta de Auditoria).
* **Categorização:** Organização de produtos por categorias com filtragem visual (Badges).

### 🔹 Movimentações
* **Entrada/Saída Padrão:** Registro formal com validação de CPF e Limite Diário (máx. 3 retiradas por CPF).
* **Saída Rápida (Mobile):** * Interface simplificada com botões grandes e stepper de quantidade (+/-).
    * **Selects Encadeados:** Ao selecionar a Categoria, o campo Produto atualiza automaticamente via JavaScript.
    * Fluxo ágil sem exigência de CPF.
* **Proteção de Estoque:** O sistema impede matematicamente (no Banco e na Aplicação) que o saldo fique negativo.

### 🔹 Controle de Acesso (RBAC)
* **Superusuários (Admins):** Acesso total (Dashboard, Histórico, Configurações, Admin Panel).
* **Usuários Comuns:** Acesso restrito apenas à tela de **Saída Rápida** (redirecionamento automático ao logar).

### 🔹 Relatórios
* **Histórico Auditável:** Rastreabilidade completa com filtros avançados.
* **Exportação CSV (WYSIWYG):** Gera planilhas Excel baseadas exatamente nos filtros aplicados na tela.

### 🔹 UI/UX
* **Dark Mode:** Tema escuro/claro persistente integrado.
* **Admin Gourmet:** Interface administrativa customizada com **Django Jazzmin**.
* **Responsividade:** Built-in com Bootstrap 5.3.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.12+, Django 5.
* **Gerenciador de Pacotes:** pip (Standard).
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3.
* **Deploy:** Vercel (Serverless Functions via `api/index.py`).
* **Database:** Neon.tech (PostgreSQL)
* **Static Files:** Whitenoise (Compressão e Cache).

---

## 📂 Estrutura do Projeto

```text
stockflow/
├── api/
│   └── index.py         # Entrypoint para Vercel (Serverless Function)
├── build_files.bash     # Script de build (instalação + static)
├── vercel.json          # Configuração de rotas e rewrites
├── requirements.txt     # Dependências do projeto
├── manage.py
├── popular_estoque.py   # Script para criar dados de teste
├── core/                # Configurações do Projeto (settings, wsgi)
└── estoque/             # Aplicação Principal
    ├── models.py        # Tabelas e Regras de Negócio (clean())
    ├── views.py         # Lógica (Transações atômicas, Filtros)
    ├── forms.py         # Formulários customizados
    └── templates/       # Telas HTML
        └── estoque/
            ├── base.html          # Template Mestre (Temas, Navbar)
            ├── dashboard.html     # Painel Admin
            ├── historico.html     # Relatórios
            └── saida_rapida.html  # Interface Mobile
```
## ⚡ Como Rodar Localmente

### 1. Clonar e Configurar
```bash
# Clone o repositório
git clone <seu-link-do-git>
cd stockflow

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar Dependências
```bash 
# Instala as bibliotecas listadas no requirements.txt
pip install -r requirements.txt
```

### 3. Banco de Dados e Usuário
```bash
# Cria as tabelas no banco de dados SQLite
python manage.py makemigrations
python manage.py migrate

# Cria um Superusuário (Para acessar Dashboard, Histórico e Admin)
python manage.py createsuperuser

# (Opcional) Popula o banco com categorias e produtos de teste
python popular_estoque.py
```
### 4. Executar
```bash
python manage.py runserver
```
Acesse no navegador: http://127.0.0.1:8000

## ☁️ Como Fazer Deploy na Vercel + Neon (PostgreSQL)

O projeto está configurado para rodar como **Serverless Function** na Vercel (via pasta `api/`) e utiliza o **Neon** como banco de dados PostgreSQL em produção.

### 1. Preparação do Banco de Dados (Neon)
1.  Crie uma conta no [Neon.tech](https://neon.tech).
2.  Crie um novo projeto e copie a **Connection String** (ex: `postgres://user:pass@ep-xyz.aws.neon.tech/neondb...`).
3.  **Importante:** Certifique-se de que seu `requirements.txt` contém `dj-database-url` e `psycopg2-binary`.

### 2. Configuração do Projeto
1.  Gere o arquivo de requisitos atualizado:
    ```bash
    pip freeze > requirements.txt
    ```
2.  Suba o projeto atualizado para o **GitHub**.

### 3. Configuração na Vercel
1.  Importe o repositório na **Vercel**.
2.  Nas configurações de **Build & Development Settings**:
    * **Framework Preset:** Other.
    * **Build/Output/Install Commands:** Deixe **VAZIO** (o `vercel.json` gerencia isso).
3.  Vá na aba **Environment Variables** e adicione:
    * `DATABASE_URL`: Cole a string de conexão do Neon.
    * `SECRET_KEY`: Gere uma chave segura aleatória.
    * `DEBUG`: Defina como `False`.
4.  Clique em **Deploy**.

### 4. Aplicando as Migrações no Neon (Pós-Deploy)
Como a Vercel é serverless, você deve rodar as migrações (criar tabelas) a partir da sua máquina local, apontando para o banco remoto:

No seu terminal local (com o venv ativado):
```bash
# Linux/Mac
export DATABASE_URL="sua-string-do-neon-aqui"
python manage.py migrate

# Windows (Powershell)
$env:DATABASE_URL = "sua-string-do-neon-aqui"
python manage.py migrate
```
Após isso, o sistema na Vercel já estará conectado e com as tabelas criadas.

## 📖 Guia de Uso

O sistema adapta a interface automaticamente dependendo do nível de permissão do usuário logado.

### 👑 Perfil: Administrador (Superusuário)
Usuários com permissão total (`is_superuser`). Ideal para gerentes de estoque.

1.  **Dashboard Geral:**
    * Visualiza a tabela completa de produtos com paginação.
    * **Filtros:** Busca por Nome, SKU ou Categoria.
    * **Status Visual:** Produtos com estoque baixo (< 5) ficam com o número em vermelho.
    * **Botão Sincronizar (⚠):** Ferramenta exclusiva que recalcula o saldo de todos os produtos somando todas as entradas e subtraindo as saídas do histórico. Use se notar inconsistências.

2.  **Registrar Movimentação (Completa):**
    * Registra Entradas ou Saídas formais.
    * Exige preenchimento de CPF (com validação automática).
    * Aplica regra de limite de 3 retiradas por dia por CPF.

3.  **Histórico e Relatórios:**
    * Tabela auditável de todas as ações feitas no sistema.
    * **Botão CSV:** Baixa uma planilha Excel contendo exatamente os dados filtrados na tela (ex: "Todas as saídas de Refrigerante em Novembro").

4.  **Painel Admin (Django):**
    * Acessível pelo botão "Admin" no cabeçalho ou via `/admin`.
    * Utilizado para criar **Categorias**, gerenciar **Usuários** e deletar registros críticos se necessário.

### 👤 Perfil: Usuário Comum (Almoxarife)
Usuários padrão (`user`). Ideal para operação rápida no chão de fábrica ou balcão.

1.  **Fluxo Simplificado:**
    * Ao fazer login, o usuário é **redirecionado automaticamente** para a tela de Saída Rápida.
    * Bloqueio de acesso: Se tentar acessar `/dashboard` ou `/historico`, o sistema o joga de volta para a saída rápida.

2.  **Saída Rápida (Interface Mobile):**
    * Desenhada para ser usada em celulares/tablets.
    * **Passo 1:** Seleciona a Categoria.
    * **Passo 2:** Seleciona o Produto (a lista atualiza automaticamente).
    * **Passo 3:** Define a quantidade com botões grandes (+ / -).
    * *Nota: Não exige CPF e não conta para o limite diário.*

---

## 🎨 Personalização (Temas)
O sistema possui suporte nativo a **Dark Mode** (Modo Escuro).
* Clique no ícone de **Lua/Sol** 🌙 na barra de navegação superior.
* A preferência é salva no navegador do usuário, mantendo o tema escolhido nos próximos acessos.

---

## 🔮 Roadmap (Futuro)

* [ ] **Registrar Nome na Movimentação:** Implementar Registro automático do nome do usuário no registro rápido, para sabermos quem realizou a movimentação.
* [ ] **Retirar Permissão Editar Histórico:** Histórico apenas servirá para auditoria e não poderá ser editado 


Melhorias planejadas para as próximas versões:

* [ ] **Dashboard Gráfico:** Implementar `Chart.js` para visualizar tendências de consumo e produtos mais retirados.
* [ ] **Notificações:** Envio de e-mail automático para o administrador quando um produto atingir o estoque mínimo.
* [ ] **Leitura de Código de Barras:** Adicionar suporte a scanner via câmera do celular na tela de Saída Rápida.
* [ ] **Auditoria de IPs:** Registrar o endereço IP de quem realizou a movimentação para maior segurança.

---

## 🤝 Contribuição

1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`).
3.  Faça o Commit (`git commit -m 'Add some AmazingFeature'`).
4.  Faça o Push (`git push origin feature/MinhaFeature`).
5.  Abra um Pull Request.

---

## 📄 Licença

Este projeto está licenciado sob a **GNU General Public License v3.0 (GPLv3)**.

Isso significa que você é livre para copiar, modificar e distribuir este software, sob as seguintes condições:
1.  **Abertura do Código:** Qualquer modificação ou trabalho derivado deve permanecer sob a mesma licença (GPLv3) e ter o código-fonte aberto.
2.  **Uso Não Comercial:** Este software é disponibilizado para uso pessoal, educacional ou interno, vedada a sua comercialização direta sem autorização prévia.

Para mais detalhes, consulte o arquivo `LICENSE` no repositório.
