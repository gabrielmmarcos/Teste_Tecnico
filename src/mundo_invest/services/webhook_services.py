from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mundo_invest.enums.enums import PrioridadeEnum, StatusEnum
from mundo_invest.models.models import Cliente, Webhook
from mundo_invest.schemas.root_schemas import FilterPage
from mundo_invest.pipefy_client.pipefy import update_pipefy_card_field_mutation


# funcao que lista todos os clientes
async def read_all_webhooks_service(session: AsyncSession, filter: FilterPage):
    # select no banco de dados com o filter que vem do endpoint
    result = await session.scalars(
        select(Webhook)
        .offset(filter.offset)
        .limit(filter.limit)
        .options(selectinload(Webhook.cliente))
    )

    webhooks = result.all()
    # retonra todos webhook encontratos
    return [
        {
            "event_id": webhook.event_id,
            "card_id": webhook.card_id,
            "timestamp": webhook.timestamp,
            "cliente_email": webhook.cliente.cliente_email,
        }
        for webhook in webhooks
    ]


# funcao de criar de webhook
async def create_webhook_service(
    webhook,
    session: AsyncSession,
):
    # verifica se o evento já existe no banco de dados
    db_webhook = await session.scalar(
        select(Webhook).where(Webhook.event_id == webhook.event_id)
    )

    if db_webhook:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Evento já processado!  Tente criar outro evento.",
        )
    # verifica se o email informado existe no banco
    cliente = await session.scalar(
        select(Cliente).where(Cliente.cliente_email == webhook.cliente_email)
    )

    if not cliente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Cliente não encontrado! Tente digitar outro email",
        )

    VALOR_PRIORIDADE_ALTA = 200000
    # regra de negocio
    if cliente.valor_patrimonio >= VALOR_PRIORIDADE_ALTA:
        cliente.prioridade = PrioridadeEnum.ALTA
    else:
        cliente.prioridade = PrioridadeEnum.NORMAL
    # altera o enum do status para processado
    cliente.status = StatusEnum.PROCESSADO
    
    # # payload para atualizar status no Pipefy
    # status_payload = update_pipefy_card_field_mutation(
    #     webhook.card_id,
    #     "status",
    #     cliente.status.value,
    # )

    # # payload para atualizar prioridade no Pipefy
    # prioridade_payload = update_pipefy_card_field_mutation(
    #     webhook.card_id,
    #     "prioridade",
    #     cliente.prioridade.value,
    # )

    # cria a instância do cliente com os dados recebidos
    novo_webhook = Webhook(
        event_id=webhook.event_id,
        card_id=webhook.card_id,
        cliente_id=cliente.id,
        cliente=cliente,
    )
    # adiciona o cliente na sessão do banco
    session.add(novo_webhook)
    # salva as alterações no banco de dados
    await session.commit()
    # atualiza os dados do objeto com as informações do banco
    await session.refresh(cliente)

    # retonar o cliente
    return cliente
