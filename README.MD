# Agenda Medica - Sistema de Agendamentos

Aplicacao web desenvolvida em Python com Flask para gestao e visualizacao de consultas medicas. O sistema possui autenticacao de usuarios, integracao com API REST de agendamentos, tabela dinamica para busca/ordenacao em tempo real e containerizacao completa com Docker.

---

## Tecnologias Utilizadas

* Backend: Python 3.10, Flask
* Banco de Dados e ORM: SQLite, Flask-SQLAlchemy
* Autenticacao e Seguranca: Flask-Login, Werkzeug (Password Hashing)
* Frontend: HTML5, CSS3, Tabulator.js (Arquivos mantidos localmente na pasta static/ sem dependencias de CDN)
* Containerizacao: Docker, Docker Compose, Gunicorn
* Testes: Unittest (Biblioteca nativa do Python)

---

## Credenciais do Usuario de Teste

O banco de dados de desenvolvimento pode ser populado utilizando o script seed.py.

| Usuario | Senha |
| :--- | :--- |
| admin | senha123 |

(Nota: O login pode ser realizado tanto utilizando o nome de usuario admin quanto o e-mail de cadastro).

---

## Como Executar o Projeto com Docker

### Pre-requisitos
* Docker e Docker Compose instalados e em execucao.

### Passos para execucao:

1. Clone o repositorio:
   git clone https://github.com/FabioJLimaJ/agenda-medica.git
   cd agenda-medica

2. Sube o container da aplicacao:
   docker compose up --build

3. Acesse a aplicacao no navegador:
   http://localhost:5000

---

## Como Executar os Testes Automatizados

O projeto conta com suite de testes automatizados utilizando unittest e banco de dados temporario isolado em memoria RAM (sqlite:///:memory:).

Para rodar os testes, execute no terminal:

python -m unittest teste_app.py

### Casos de testes cobertos:
* test_login: Valida a autenticacao com credenciais corretas e o redirecionamento para a agenda.
* test_login_incorreto: Valida o tratamento de falha ao inserir senhas invalidas.
* test_api: Testa o retorno do endpoint /api/agendamentos e valida a presenca das chaves obrigatorias no JSON.

---

## Decisoes Tecnicas e Arquitetura

1. Dependencias Frontend Locais (static/):
   * Os arquivos JS e CSS do Tabulator e bibliotecas auxiliares foram armazenados localmente na pasta static/ para garantir autonomia total da interface, permitindo que a aplicacao funcione em ambientes restritos ou offline (sem consumo de CDN externas).

2. Servidor Gunicorn em Container:
   * Para a execucao no Docker, foi configurado o Gunicorn com suporte a threads/multiprocessamento. Isso evita travamentos e conexoes presas (deadlocks) ao realizar requisicoes internas HTTP a propria API no container.

3. Validacao de Payload e Resiliencia da API:
   * A rota /agenda realiza o consumo da API interna e conta com tratamento estrito de excecoes (try/except com suporte a Timeout e RequestException).
   * Adicionalmente, e feita a checagem dinamica das chaves do dicionario para ignorar registros que venham com campos obrigatorios ausentes no JSON.