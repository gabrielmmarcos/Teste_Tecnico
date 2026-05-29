from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.enums.enums import (
    PrioridadeEnum,
    StatusEnum,
)
from mundo_invest.models.models import Cliente
from mundo_invest.schemas.webhook_schemas import (
    WebhookResponse,
)
from mundo_invest.services.webhook_services import (
    create_webhook_service,
)


# teste para validar regra de prioridade
@pytest.mark.asyncio
async def test_create_webhook_prioridade_alta(
    session: AsyncSession,
):
    # cria cliente com patrimonio alto
    cliente = Cliente(
        cliente_nome="Gabriel Marcos",
        cliente_email="gabriel@gmail.com",
        tipo_solicitacao="entrada",
        valor_patrimonio=300000,
    )

    session.add(cliente)
    await session.commit()

    # payload do webhook
    webhook_payload = WebhookResponse(
        event_id="evento-123",
        card_id="card-123",
        cliente_email="gabriel@gmail.com",
        timestamp=datetime.now(),
    )

    # processa webhook
    cliente_processado = await create_webhook_service(
        webhook_payload,
        session,
    )

    # verifica prioridade
    assert cliente_processado.prioridade == PrioridadeEnum.ALTA

    # verifica status
    assert cliente_processado.status == StatusEnum.PROCESSADO
