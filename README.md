# Mundo Invest - Internal Management API
Sistema interno para gerenciamento de clientes, controle de patrimônio investido e mapeamento de processos.

## Visão Geral
A API Mundo Invest é um sistema construído com FastAPI e PostgreSQL que permite:

- Gerenciamento de Clientes: Criar e listar clientes com dados de patrimônio e tipo de solicitação
- Processamento de Webhooks: Receber e processar eventos de webhooks do Pipefy para atualizar prioridade de clientes
- Análise de Priorização: Sistema inteligente que classifica clientes por prioridade baseado em eventos

## Quickstart - Execução com Docker (recomendado)

### Pré-requisitos

* Docker
* Docker Compose

---

#### 1. Clonar o repositório

```bash
git clone <repository-url>
cd mundo-invest
```

---

#### 2. Configurar variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto:

```env
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password
POSTGRES_DB=app_db

# URL para execução via Docker
DATABASE_URL=postgresql+psycopg://app_user:app_password@app_database:5432/app_db

# URL para execução local sem Docker
# DATABASE_URL=postgresql+psycopg://app_user:app_password@localhost:5432/app_db
```

---

#### 3. Executar a aplicação

```bash
docker-compose up --build
```

A aplicação iniciará automaticamente com:

* PostgreSQL na porta `5432`
* FastAPI na porta `8000`
* Migrações Alembic executadas automaticamente
* Dependências instaladas automaticamente

---

#### 4. Acessar a aplicação

API:

```txt
http://localhost:8000
```

Swagger UI:

```txt
http://localhost:8000/docs
```

## Quickstart - Execução Local

### Pré-requisitos

* Python 3.13+
* Docker & Docker Compose
* Poetry (gerenciador de pacotes)

---

#### 1. Clonar o repositório

```bash
git clone <repository-url>
cd mundo-invest
```

---

#### 2. Configurar variáveis de ambiente

Criar arquivo `.env` na raiz do projeto:

```env
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password
POSTGRES_DB=app_db

# URL para execução local
# DATABASE_URL=postgresql+psycopg://app_user:app_password@localhost:5432/app_db

# URL para execução via Docker
DATABASE_URL=postgresql+psycopg://app_user:app_password@app_database:5432/app_db
```

---

#### 3. Subi o banco de dados (PostgreSQL + API)

```bash
docker-compose up --build
```

Isso iniciará:

* PostgreSQL na porta 5432
* API FastAPI na porta 8000

---

#### 4. Instalar dependências

```bash
poetry install
```

---

#### 5. Executar migrações do banco de dados

```bash
poetry run alembic upgrade head
```

---

#### 6. Executar a aplicação

### Usando taskipy (recomendado)

```bash
poetry run task run
```

---

#### 7. Acessar a aplicação

API:

```txt
http://127.0.0.1:8000
```

Swagger UI:

```txt
 http://127.0.0.1:8000/docs
```


## Executar Testes
### Executar todos os testes com cobertura
poetry run task test

### Testes disponíveis:

test_app.py - Testes de endpoints da API
test_client.py - Teste de criação de cliente
test_webhook_prioridade.py - Teste de priorização via webhook
test_webhook_duplicate.py - Teste de prevenção de webhooks duplicados
test_db.py - Teste de integração com banco de dados

## Exemplos de Requisição (curl)

---

### Endpoint 1: Criar Cliente

`POST /clientes/criar_cliente`

Cria um novo cliente no sistema com informações de patrimônio e tipo de solicitação.

#### Exemplo de requisição

```bash
curl -X POST "http://127.0.0.1:8000/clientes/criar_cliente" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Consultoria",
    "valor_patrimonio": 50000.00
  }'
```

#### Resposta esperada (201 Created)

```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Consultoria",
  "valor_patrimonio": 50000.00,
  "status": "AGUARDANDO_ANALISE",
  "prioridade": null
}
```

### Campos da requisição

| Campo            | Tipo   | Descrição                           | Requerido |
| ---------------- | ------ | ----------------------------------- | --------- |
| cliente_nome     | string | Nome completo do cliente            | ✅         |
| cliente_email    | string | Email válido do cliente             | ✅         |
| tipo_solicitacao | string | Tipo de solicitação/serviço         | ✅         |
| valor_patrimonio | float  | Valor total do patrimônio investido | ✅         |

---

## Endpoint 2: Webhook - Atualizar Prioridade

`POST /webhooks/pipefy/card-updated`

Processa eventos de webhooks do Pipefy para atualizar a prioridade de um cliente existente.

#### Exemplo de requisição

```bash
curl -X POST "http://127.0.0.1:8000/webhooks/pipefy/card-updated" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_12345",
    "card_id": "card_67890",
    "timestamp": "2024-05-28T15:30:00Z",
    "cliente_email": "joao.silva@example.com"
  }'
```

#### Resposta esperada (200 OK)

```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Consultoria",
  "valor_patrimonio": 50000.00,
  "status": "PROCESSADO",
  "prioridade": "ALTA"
}
```

#### Campos da requisição

| Campo         | Tipo   | Descrição                      | Requerido |
| ------------- | ------ | ------------------------------ | --------- |
| event_id      | string | ID único do evento             | ✅         |
| card_id       | string | ID do card no Pipefy           | ✅         |
| timestamp     | string | Data/hora do evento (ISO 8601) | ✅         |
| cliente_email | string | Email do cliente para vincular | ✅         |

---

## Endpoint 3: Listar Clientes

`GET /clientes/all`

Lista todos os clientes cadastrados com suporte a paginação.

### Exemplo de requisição

#### Listar todos os clientes

```bash
curl -X GET "http://127.0.0.1:8000/clientes/all?skip=0&limit=10" \
  -H "Content-Type: application/json"
```

#### Resposta esperada

```json
{
  "clientes": [
    {
      "cliente_nome": "João Silva",
      "cliente_email": "joao.silva@example.com",
      "tipo_solicitacao": "Consultoria",
      "valor_patrimonio": 50000.00,
      "status": "PROCESSADO",
      "prioridade": "ALTA"
    }
  ]
}
```

---

## Endpoint 4: Listar Webhooks

`GET /webhooks/all`

Lista todos os eventos de webhook processados.

#### Exemplo de requisição

```bash
curl -X GET "http://127.0.0.1:8000/webhooks/all?skip=0&limit=10" \
  -H "Content-Type: application/json"
```

#### Resposta esperada

```json
{
  "webhooks": [
    {
      "event_id": "evt_12345",
      "card_id": "card_67890",
      "timestamp": "2024-05-28T15:30:00Z",
      "cliente_email": "joao.silva@example.com"
    }
  ]
}
```

## Produção na AWS

### Arquitetura Escalável na Cloud

Esta solução foi projetada com princípios de escalabilidade em mente. Na AWS, a arquitetura escalaria conforme descrito abaixo.

---

#### 1. Computação (Serverless com Lambda)

Em vez de executar um servidor FastAPI tradicional, utilizaríamos:

* AWS Lambda para cada operação:

  * Criar cliente
  * Processar webhook
  * Listar dados

#### Vantagens

* Escalabilidade automática
* Pay-per-use
* Sem gerenciamento de servidores
* Alta disponibilidade nativa

#### Configuração

* Runtime Python 3.13+
* FastAPI + Mangum (adaptador ASGI)

#### Concorrência

* Suporte para milhões de requisições simultâneas

---

### 2. Gateway de API (API Gateway)

#### API Gateway REST

Responsável por:

* Roteamento das requisições
* Autenticação
* Rate limiting
* Controle de CORS
* Cache de respostas

#### Recursos

* IAM
* API Keys
* Cognito
* CloudFront cache

---

### 3. Banco de Dados

#### Amazon RDS (PostgreSQL)

##### Benefícios

* PostgreSQL gerenciado
* Auto Scaling
* Multi-AZ
* Backups automáticos
* Read replicas


### 4. Processamento Assíncrono de Webhooks

#### SQS (Simple Queue Service)

Fluxo:

```txt id="6ttht1"
Webhook → SQS → Lambda Worker → DynamoDB
```

##### Benefícios

* Retry automático
* Dead Letter Queue (DLQ)
* Garantia "at-least-once"

---

#### SNS (Simple Notification Service)

Responsável por:

* Publicar eventos processados
* Notificações em tempo real
* Integração com Email, SMS e Lambdas

---

### 5. Armazenamento e Logs

#### Serviços utilizados

* S3 → backups e auditoria
* CloudWatch → logs centralizados
* X-Ray → tracing distribuído
* CloudTrail → auditoria de APIs

---

### 6. Segurança e Rede

#### Recursos AWS

* VPC Endpoints
* Secrets Manager
* AWS KMS
* AWS WAF

#### Proteções

* SQL Injection
* XSS
* Controle de acesso
* Criptografia de dados

---

### 7. Escalabilidade Esperada

| Métrica           | Local  | AWS        |
| ----------------- | ------ | ---------- |
| Requisições/seg   | ~100   | 1.000.000+ |
| Tempo de resposta | ~200ms | ~50ms      |
| Disponibilidade   | 99%    | 99.99%     |
| Setup             | 1 dia  | 2-3 dias   |

---

### 8. Diagrama da Arquitetura AWS

![Arquitetura AWS](./assets/aws-architecture.png)

---

### 9. Migração de Local para AWS

#### Passo 1

Refatorar FastAPI para Lambda com Mangum:

```python id="0pn4g8"
from mangum import Mangum

handler = Mangum(app)
```

---

#### Passo 2

Substituir:

* SQLAlchemy
* PostgreSQL

Por:

* Boto3
* DynamoDB

---

#### Passo 3

Implementar processamento assíncrono com:

* SQS
* SNS
* Workers Lambda

---

#### Passo 4

Deploy utilizando:

* AWS SAM
* Terraform

---

#### 10. Estimativa de Custos (AWS)

| Serviço       | Estimativa          |
| ------------- | ------------------- |
| Lambda        | $0.20 / 1M requests |
| DynamoDB      | $1.25 / GB          |
| API Gateway   | $3.50 / 1M requests |
| Data Transfer | $0.09 / GB          |

#### Estimativa total

```txt id="kl7yrd"
~ $100 - $500/mês para 10M requests/mês
```

## Estrutura do Projeto
mundo-invest/
├── src/
│   ├── mundo_invest/
│   │   ├── app.py                 # App principal FastAPI
│   │   ├── database.py            # Configuração de banco de dados
│   │   ├── settings.py            # Variáveis de ambiente
│   │   ├── models/
│   │   │   └── models.py          # Modelos SQLAlchemy (Cliente, Webhook)
│   │   ├── schemas/               # Schemas Pydantic (validação)
│   │   │   ├── cliente_schemas.py
│   │   │   ├── webhook_schemas.py
│   │   │   └── root_schemas.py
│   │   ├── routers/               # Rotas da API
│   │   │   ├── cliente_router.py
│   │   │   └── webhook_router.py
│   │   ├── services/              # Lógica de negócio
│   │   │   ├── cliente_services.py
│   │   │   └── webhook_services.py
│   │   ├── enums/
│   │   │   └── enums.py           # Enums (Status, Prioridade)
│   │   └── pipefy_client/
│   │       └── pipefy.py          # Integração Pipefy
│   └── tests/                     # Testes unitários e integração
│       ├── conftest.py
│       ├── test_app.py
│       ├── test_client.py
│       ├── test_webhook_prioridade.py
│       └── test_webhook_duplicate.py
├── migrations/                    # Migrações Alembic
├── .env                          # Variáveis de ambiente
├── .gitignore
├── Dockerfile                    # Build da aplicação
├── compose.yaml                  # Docker Compose (PostgreSQL + API)
├── pyproject.toml               # Configuração Poetry e dependências
├── alembic.ini                  # Configuração Alembic
├── entrypoint.sh                # Script de inicialização
└── README.md                    # Este arquivo


## Dependências Principais
FastAPI: Web framework moderno
SQLAlchemy: ORM assíncrono
Pydantic: Validação de dados
Alembic: Gerenciamento de migrações
psycopg: Driver PostgreSQL assíncrono
Pytest: Framework de testes
Ruff: Linter e formatador
Veja pyproject.toml para versões exatas.
