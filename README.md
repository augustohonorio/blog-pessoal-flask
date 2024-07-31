# Blog Pessoal

Este é um projeto de um blog pessoal construído com Flask e Boostrap.
Ele permite que os usuários registrem contas, criem, editem e excluam postagens, e um painel de administração para gerenciar usuários e possibilitando habilitar ou desabilitar o registro de novos usuários. 
O intuito dele é para ser usado por pessoas individuais. Por este fator não foi implementado controle de postagens. Embora permita mais de uma pessoa cadastrar para poder postar no blog se caso for necessário.
Lembrando que este projeto são apenas para fins de estudo e/ou utilização pessoal. Onde cada usuário ao usar este sistema sendo responsável pelas suas próprias postagens, deixando este que vos fala, isento de qualquer responsabilidade da utilização do mesmo.

## Funcionalidades

- Registro e login de usuários
- Criação, edição e exclusão de postagens
- Painel de administração para promover usuários a administradores e deletar contas;
- Controle de habilitação de registro de novos usuários;
- O primeiro usuário registrado será automaticamente um administrador.
- Cada usuário só poderá editar seus próprios posts ou excluí-los
- Tema escuro (Economizar a visão é bom e os olhos agradecem.)

## Estrutura do Projeto

- `app/`
  - `__init__.py`: Inicializa a aplicação Flask e configura extensões.
  - `models.py`: Define os modelos de dados.
  - `routes.py`: Define as rotas da aplicação.
  - `forms.py`: Define os formulários usados na aplicação.
  - `templates/`: Contém os arquivos HTML renderizados.
  - `static/`: Contém arquivos estáticos como CSS e JavaScript.
- `migrations/`: Contém scripts de migração do banco de dados.
- `config.py`: Configurações da aplicação.
- `run.py`: Ponto de entrada para rodar a aplicação.

## Configurações

O arquivo `config.py` contém as configurações da aplicação, como a URL do banco de dados e a chave secreta para o Flask-WTF.

## Instalação

1. Clone o repositório:
   git clone (LINK DO REPOSITÓRIO)
   cd blog-pessoal

2. Crie e ative um ambiente virtual:
    python -m venv venv
    source venv/bin/activate

3. Instale as dependências:
    pip install -r requirements.txt

4. Configure as variáveis de ambiente:
    export FLASK_APP=run.py
    export FLASK_ENV=development

5. Inicialize o banco de dados:
    flask db init
    flask db upgrade

6. Rode a aplicação:
    flask run

## Imagens do sistema
![image](https://github.com/user-attachments/assets/a5807abc-b0c3-4a36-9c9d-91744b72283d)
![image](https://github.com/user-attachments/assets/f22a8196-b9a1-47b8-bc5b-542c527a61b1)


   


Use com responsabilidade amiguinho :-)
