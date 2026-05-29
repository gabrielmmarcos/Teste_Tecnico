from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.enums.enums import StatusEnum
from mundo_invest.models.models import Cliente
from mundo_invest.schemas.cliente_schemas import ClientePublic
from mundo_invest.services.cliente_services import (
    create_client_service,
)


# teste para criar cliente com payload válido
@pytest.mark.asyncio
async def test_create_client_service(session: AsyncSession):
    # payload simulando criação do cliente
    cliente_payload = ClientePublic(
        cliente_nome="Gabriel Marcos",
        cliente_email="gabriel@gmail.com",
        tipo_solicitacao="entrada",
        valor_patrimonio=1000,
    )

    # cria cliente
    await create_client_service(cliente_payload, session)

    # busca cliente no banco
    db_cliente = await session.scalar(
        select(Cliente).where(Cliente.cliente_email == "gabriel@gmail.com")
    )

    # verifica se cliente existe
    assert db_cliente is not None

    # verifica dados do cliente
    assert asdict(db_cliente) == {
        "id": 1,
        "cliente_nome": "Gabriel Marcos",
        "cliente_email": "gabriel@gmail.com",
        "tipo_solicitacao": "entrada",
        "valor_patrimonio": 1000,
        "status": StatusEnum.AGUARDANDO_ANALISE,
        "prioridade": None,
    }
