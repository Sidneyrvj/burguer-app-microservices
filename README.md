# 🍔 Burguer App - Sistema de Pedidos com Microserviços

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-96-success.svg)](https://github.com/)
[![Coverage](https://img.shields.io/badge/Coverage-91%25-brightgreen.svg)](https://github.com/)

> Sistema completo de gestão de pedidos de hamburgueria construído com arquitetura de microserviços, 96 testes automatizados e 91% de cobertura de código.

---

## 📋 Sobre o Projeto

Sistema de gerenciamento de pedidos desenvolvido com **arquitetura de microserviços**, utilizando **Flask**, **MongoDB** e **Docker**. O projeto implementa funcionalidades completas de CRUD para usuários, produtos e pedidos, com autenticação JWT e testes automatizados.

### 🎯 Destaques

- ✅ **96 testes automatizados** com pytest
- ✅ **91% de cobertura de código média**
- ✅ **2 serviços com 100% de cobertura**
- ✅ **Arquitetura de microserviços**
- ✅ **Docker Compose** para orquestração
- ✅ **Autenticação JWT**
- ✅ **API RESTful**

---

## 🏗️ Arquitetura

O projeto é dividido em **4 microserviços independentes**:

\\\
burguer-app/
├── user-service/          # Gestão de usuários
├── auth-service/          # Autenticação e sessões
├── order-service/         # Gerenciamento de pedidos
└── product-service/       # Catálogo de produtos
\\\

### 📊 Cobertura de Testes por Serviço

| Serviço | Testes | Cobertura | Status |
|---------|--------|-----------|--------|
| **user-service** | 14 | 80% | ✅ |
| **order-service** | 25 | 85% | ✅ |
| **auth-service** | 22 | 100% | 🔥 |
| **product-service** | 35 | 100% | 🔥 |
| **TOTAL** | **96** | **91%** | ✅ |

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.13**
- **Flask 3.0** - Framework web
- **Flask-CORS** - Cross-Origin Resource Sharing
- **PyMongo** - Driver MongoDB para Python
- **PyJWT** - Autenticação JWT
- **Werkzeug** - Segurança e hashing de senhas

### Banco de Dados
- **MongoDB 7.0** - Banco de dados NoSQL

### Testes
- **Pytest** - Framework de testes
- **Pytest-cov** - Cobertura de código
- **Pytest-flask** - Testes Flask
- **Pytest-mock** - Mocking

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

---

## 📦 Instalação e Execução

### Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.13+ (para desenvolvimento local)
- MongoDB (ou usar via Docker)

### 1️⃣ Clone o Repositório

\\\ash
git clone https://github.com/seu-usuario/burguer-app.git
cd burguer-app
\\\

### 2️⃣ Configure as Variáveis de Ambiente

Crie um arquivo \.env\ em cada serviço:

\\\env
MONGO_URI=mongodb://localhost:27017
JWT_SECRET=sua_chave_secreta_aqui
\\\

### 3️⃣ Suba os Containers com Docker Compose

\\\ash
docker-compose up -d
\\\

### 4️⃣ Acesse os Serviços

- **User Service**: http://localhost:5001
- **Auth Service**: http://localhost:5002  
- **Order Service**: http://localhost:5003
- **Product Service**: http://localhost:5004

---

## 🧪 Executar Testes

### Rodar Todos os Testes

\\\ash
# Em cada serviço
cd user-service
python -m pytest test/ -v --cov

cd ../order-service
python -m pytest test/ -v --cov

cd ../auth-service
python -m pytest test/ -v --cov

cd ../product-service
python -m pytest test/ -v --cov
\\\

### Cobertura Detalhada

\\\ash
python -m pytest test/ -v --cov --cov-report=html
\\\

---

## 📡 API Endpoints

### User Service (Porta 5001)

- \POST /user/create\ - Criar usuário
- \GET /user/list\ - Listar usuários
- \GET /user/<id>\ - Buscar usuário
- \POST /user/update/<id>\ - Atualizar usuário
- \POST /user/delete/<id>\ - Deletar usuário

### Auth Service (Porta 5002)

- \POST /auth/login\ - Fazer login
- \GET /auth/dashboard\ - Dashboard do usuário
- \GET /auth/logout\ - Fazer logout

### Order Service (Porta 5003)

- \POST /order/create\ - Criar pedido
- \GET /order/list\ - Listar pedidos
- \GET /order/details/<id>\ - Detalhes do pedido
- \POST /order/update_status/<id>\ - Atualizar status
- \POST /order/delete/<id>\ - Deletar pedido

### Product Service (Porta 5004)

- \GET /product/list\ - Listar produtos
- \POST /product/create\ - Criar produto
- \GET /product/edit/<id>\ - Editar produto
- \POST /product/delete/<id>\ - Deletar produto
- \GET /product/api/products\ - API JSON produtos
- \GET /product/api/categories\ - API JSON categorias

---

## 🎨 Funcionalidades

### 👤 Gestão de Usuários
- Cadastro de usuários com validação
- Perfis: cliente e administrador
- Criptografia de senhas com Werkzeug
- CRUD completo

### 🔐 Autenticação
- Login com JWT
- Sessões persistentes
- Controle de acesso por role
- 100% de cobertura de testes

### 🍔 Catálogo de Produtos
- Categorização de produtos
- Gestão de disponibilidade
- Ingredientes e preços
- API JSON para integração
- 100% de cobertura de testes

### 📋 Gestão de Pedidos
- Criação de pedidos multi-item
- Status do pedido (pendente, preparando, pronto, entregue)
- Histórico por usuário
- Validação de usuários

---

## 🧪 Estrutura de Testes

Cada serviço possui testes completos:

\\\
service/
├── test/
│   ├── test_service.py      # Testes da lógica de negócio
│   ├── test_controller.py   # Testes das rotas Flask
│   ├── test_model.py        # Testes de serialização
│   └── conftest.py          # Configurações do pytest
├── pytest.ini               # Configuração do pytest
└── .coveragerc             # Configuração de cobertura
\\\

### Exemplo de Teste

\\\python
def test_create_user_success(mock_users_col):
    mock_users_col.find_one.return_value = None
    mock_users_col.insert_one.return_value = MagicMock(inserted_id=ObjectId())

    response, status = create_user('Sidney Rodrigues', 'sidney@gmail', 'senha123')

    assert status == 201
    assert 'message' in response
\\\

---

## 🛠️ Desenvolvimento Local

### Instalar Dependências

\\\ash
cd user-service
pip install -r requirements.txt
\\\

### Executar Serviço Localmente

\\\ash
python app.py
\\\

### Executar Testes com Watch Mode

\\\ash
ptw -- -v --cov
\\\

---

## 📈 Próximos Passos

- [ ] CI/CD com GitHub Actions
- [ ] Testes de integração entre serviços
- [ ] Frontend React/Vue
- [ ] Kubernetes deployment
- [ ] API Gateway
- [ ] Rate limiting
- [ ] Logging centralizado
- [ ] Métricas e monitoramento

---

## 👨‍💻 Autor

**Sidney** - [GitHub](https://github.com/Sidneyrvj) | [LinkedIn](www.linkedin.com/in/sidney-rodrigues-0b18a0334)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

Projeto desenvolvido como parte do aprendizado em arquitetura de microserviços e boas práticas de desenvolvimento com testes automatizados.

---

**⭐ Se este projeto te ajudou, deixe uma estrela no repositório!**
