from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.models.models import (
    Cliente,
    Webhook,
)
from mundo_invest.schemas.webhook_schemas import (
    WebhookResponse,
)
from mundo_invest.services.webhook_services import (
    create_webhook_service,
)


# teste para verificar webhook duplicado
@pytest.mark.asyncio
async def test_create_webhook_duplicate_event(
    session: AsyncSession,
):
    # cria cliente
    cliente = Cliente(
        cliente_nome="Gabriel Marcos",
        cliente_email="gabriel@gmail.com",
        tipo_solicitacao="entrada",
        valor_patrimonio=50000,
    )

    session.add(cliente)
    await session.commit()

    # cria webhook
    webhook = Webhook(
        event_id="evento-duplicado",
        card_id="card-1",
        cliente_id=cliente.id,
        cliente=cliente
    )

    session.add(webhook)
    await session.commit()

    # payload webhook duplicado
    webhook_payload = WebhookResponse(
        event_id="evento-duplicado",
        card_id="card-2",
        cliente_email="gabriel@gmail.com",
        timestamp=datetime.now(),
    )

    # verifica exceção
    with pytest.raises(HTTPException) as exc:
        await create_webhook_service(
            webhook_payload,
            session,
        )

    # valida status code
    assert exc.value.status_code == HTTPStatus.CONFLICT

    # valida mensagem
    assert (
        exc.value.detail == "Evento já processado!  Tente criar outro evento."
    )
