Mundo Invest - Internal Management API
Sistema interno para gerenciamento de clientes, controle de patrimônio investido e mapeamento de processos.

📋 Visão Geral
A API Mundo Invest é um sistema construído com FastAPI e PostgreSQL que permite:

Gerenciamento de Clientes: Criar e listar clientes com dados de patrimônio e tipo de solicitação
Processamento de Webhooks: Receber e processar eventos de webhooks do Pipefy para atualizar prioridade de clientes
Análise de Priorização: Sistema inteligente que classifica clientes por prioridade baseado em eventos
🚀 Quickstart - Execução Local
Pré-requisitos
Python 3.13+
Docker & Docker Compose
Poetry (gerenciador de pacotes)
Instalação e Execução
1. Clonar o repositório
git clone <repository-url>
cd mundo-invest
2. Configurar variáveis de ambiente
Criar arquivo .env na raiz do projeto:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mundo_invest
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mundo_invest
3. Iniciar serviços (PostgreSQL)
docker-compose up -d
Isso iniciará:

PostgreSQL na porta 5432
API FastAPI na porta 8000
4. Instalar dependências
poetry install
5. Executar migrações do banco de dados
# Com poetry
poetry run alembic upgrade head
6. Executar a aplicação
# Usando taskipy (recomendado)
poetry run task run

# Ou diretamente com FastAPI dev server
poetry run fastapi dev src/mundo_invest/app.py
A API estará disponível em: http://localhost:8000

Documentação interativa (Swagger UI): http://localhost:8000/docs

🧪 Executar Testes
# Executar todos os testes com cobertura
poetry run task test

# Executar testes com verbose
poetry run pytest -vv

# Gerar relatório de cobertura HTML
poetry run pytest --cov=src --cov-report=html
Testes disponíveis:

test_app.py - Testes de endpoints da API
test_client.py - Testes do serviço de clientes
test_webhook_prioridade.py - Testes de priorização via webhook
test_webhook_duplicate.py - Testes de prevenção de webhooks duplicados
test_db.py - Testes de integração com banco de dados
📝 Linting e Formatação
# Executar linter (Ruff)
poetry run task lint

# Formatar código
poetry run task format
📡 Exemplos de Requisição (curl)
Endpoint 1: Criar Cliente
POST /clientes/criar_cliente

Cria um novo cliente no sistema com informações de patrimônio e tipo de solicitação.

Exemplo de requisição:

curl -X POST "http://localhost:8000/clientes/criar_cliente" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Consultoria",
    "valor_patrimonio": 50000.00
  }'
Resposta esperada (201 Created):

{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Consultoria",
  "valor_patrimonio": 50000.00,
  "status": "AGUARDANDO_ANALISE",
  "prioridade": null
}
Campos da requisição:

Campo	Tipo	Descrição	Requerido
cliente_nome	string	Nome completo do cliente	✅
cliente_email	string	Email válido do cliente	✅
tipo_solicitacao	string	Tipo de solicitação/serviço	✅
valor_patrimonio	float	Valor total do patrimônio investido	✅
Endpoint 2: Webhook - Atualizar Prioridade (Pipefy)
POST /webhooks/pipefy/card-updated

Processa eventos de webhooks do Pipefy para atualizar a prioridade de um cliente existente.

Exemplo de requisição:

curl -X POST "http://localhost:8000/webhooks/pipefy/card-updated" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_12345",
    "card_id": "card_67890",
    "timestamp": "2024-05-28T15:30:00Z",
    "cliente_email": "joao.silva@example.com"
  }'
Resposta esperada (200 OK):

{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Consultoria",
  "valor_patrimonio": 50000.00,
  "status": "AGUARDANDO_ANALISE",
  "prioridade": "ALTA"
}
Campos da requisição:

Campo	Tipo	Descrição	Requerido
event_id	string	ID único do evento	✅
card_id	string	ID do card no Pipefy	✅
timestamp	string	Data/hora do evento (ISO 8601)	✅
cliente_email	string	Email do cliente para vincular	✅
Endpoint 3: Listar Clientes
GET /clientes/all

Lista todos os clientes cadastrados com suporte a paginação.

Exemplo de requisição:

# Listar todos os clientes
curl -X GET "http://localhost:8000/clientes/all" \
  -H "Content-Type: application/json"

# Com paginação (skip=0, limit=10)
curl -X GET "http://localhost:8000/clientes/all?skip=0&limit=10" \
  -H "Content-Type: application/json"
Resposta esperada:

{
  "clientes": [
    {
      "cliente_nome": "João Silva",
      "cliente_email": "joao.silva@example.com",
      "tipo_solicitacao": "Consultoria",
      "valor_patrimonio": 50000.00,
      "status": "AGUARDANDO_ANALISE",
      "prioridade": "ALTA"
    }
  ]
}
Endpoint 4: Listar Webhooks
GET /webhooks/all

Lista todos os eventos de webhook processados.

Exemplo de requisição:

curl -X GET "http://localhost:8000/webhooks/all?skip=0&limit=10" \
  -H "Content-Type: application/json"
Resposta esperada:

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
🌍 Visão de Produção na AWS
Arquitetura Escalável na Cloud
Esta solução foi projetada com princípios de escalabilidade em mente. Na AWS, a arquitetura escalaria conforme descrito abaixo:

1. Computação (Serverless com Lambda)
Em vez de executar um servidor FastAPI tradicional, usaríamos:

AWS Lambda: Funções serverless para cada operação (criar cliente, processar webhook, listar dados)
Vantagem: Escalabilidade automática, pay-per-use, sem gerenciamento de servidor
Configuração: Runtime Python 3.13+ com FastAPI + Mangum (adaptador ASGI)
Concorrência: Suporta milhões de requisições simultâneas
2. Gateway de API (API Gateway)
API Gateway REST: Roteamento de requisições para funções Lambda
Autenticação: IAM, API Keys, Cognito
Rate Limiting: Proteção contra abuso
CORS: Habilitado para frontend da web
Cache: Respostas GET cacheadas em CloudFront para performance
3. Banco de Dados
Opção A: Amazon RDS (PostgreSQL) - Mais simples

Instância PostgreSQL gerenciada com Auto Scaling
Multi-AZ para alta disponibilidade
Backups automáticos e snapshots
Escalabilidade: Read replicas para distribuir carga de leitura
Opção B: DynamoDB - Mais escalável (Recommended)

Banco NoSQL totalmente gerenciado
Escalabilidade automática (on-demand ou provisioned)
Baixa latência (<10ms)
Replicação global automática
Estrutura de dados:
Tabela: Clientes
- PK: cliente_email (Partition Key)
- GSI: status (para queries por status)

Tabela: Webhooks
- PK: event_id (Partition Key)
- GSI: cliente_email (para queries por cliente)
4. Processamento Assíncrono de Webhooks
Para lidar com grande volume de webhooks:

SQS (Simple Queue Service): Fila de mensagens para webhooks

Webhook entra em SQS → Lambda processa de forma assíncrona
Retry automático com Dead Letter Queue (DLQ)
Garante entrega "at-least-once"
SNS (Simple Notification Service): Notificações em tempo real

Publica eventos de webhook processados
Subscribers recebem notificações (Email, SMS, Lambda)
Fluxo de webhook:

Pipefy Webhook → API Gateway → Lambda → SQS → Processing Lambda → DynamoDB
                                                                  ↓
                                                            SNS (Notifications)
5. Armazenamento e Logs
S3: Armazena backups de dados, logs de auditoria
CloudWatch: Logs centralizados das Lambdas
X-Ray: Rastreamento distribuído para debugging
CloudTrail: Auditoria de chamadas de API
6. Segurança e Rede
VPC Endpoints: Acesso privado a AWS Services
Secrets Manager: Gerenciar credenciais de banco de dados
KMS: Criptografia de dados em repouso
WAF: Proteção contra ataques web (SQL injection, XSS, etc)
7. Escalabilidade Esperada
Métrica	Local	AWS
Requisições/seg	~100	1,000,000+
Tempo de resposta	~200ms	~50ms
Disponibilidade	99%	99.99%
Custo (mensal)	~$0	~$100-500*
Setup time	1 dia	2-3 dias
*Variável conforme volume

8. Diagrama de Arquitetura na AWS
┌─────────────────────────────────────────────────────────────────┐
│                    Pipefy / Clients                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  CloudFront + WAF   │
                    │  (Cache + Security) │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────────┐
                    │   API Gateway REST      │
                    │ (Auth + Rate Limiting)  │
                    └──────────┬──────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼────┐  ┌───────▼────┐  ┌──────▼──────┐
    │ Lambda 1     │  │ Lambda 2   │  │ Lambda 3    │
    │ (POST Client)│  │(GET Client)│  │(POST Webhook│
    └─────────┬────┘  └───────┬────┘  └──────┬──────┘
              │                │              │
              └────────────────┼──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   SQS (Webhooks)    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Lambda Worker       │
                    │ (Process Webhooks)  │
                    └──────────┬──────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼────────┐  ┌──────▼──────┐  ┌─────▼────┐
    │ DynamoDB       │  │  SNS        │  │ S3/Logs  │
    │ (Data)         │  │ (Events)    │  │ (Audit)  │
    └────────────────┘  └─────────────┘  └──────────┘
9. Migração de Local para AWS
Passo 1: Refatorar código FastAPI para suportar Lambda (Mangum)

from mangum import Mangum
handler = Mangum(app)
Passo 2: Substituir SQLAlchemy + PostgreSQL por Boto3 + DynamoDB

Passo 3: Implementar async patterns para SQS

Passo 4: Deploy com SAM (AWS Serverless Application Model) ou Terraform

10. Estimativa de Custos (AWS)
Lambda: $0.20 por 1M requisições (primeiros 1B/mês free)
DynamoDB: $1.25 por GB (on-demand)
API Gateway: $3.50 por 1M requisições
Data Transfer: $0.09 por GB
Total estimado: $100-500/mês para 10M requisições/mês
📁 Estrutura do Projeto
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
🔗 Dependências Principais
FastAPI: Web framework moderno
SQLAlchemy: ORM assíncrono
Pydantic: Validação de dados
Alembic: Gerenciamento de migrações
psycopg: Driver PostgreSQL assíncrono
Pytest: Framework de testes
Ruff: Linter e formatador
Veja pyproject.toml para versões exatas.

🤝 Contribuindo
Crie uma branch para sua feature (git checkout -b feature/amazing-feature)
Commit suas mudanças (git commit -m 'Add amazing feature')
Push para a branch (git push origin feature/amazing-feature)
Abra um Pull Request
📧 Contato
Desenvolvido por: Gabriel M. Marcos Email: gabrielmmarcos1@gmail.com

📝 Licença
Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

Última atualização: Maio 2024 