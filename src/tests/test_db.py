from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.enums.enums import StatusEnum
from mundo_invest.models.models import Cliente


# teste para confirmar se o cliente esta sendo criado no banco de dados
@pytest.mark.asyncio
async def test_create_produto(session: AsyncSession):
    # variavel para simular a criacao do cliente
    new_cliente = Cliente(
        cliente_nome="Gabriel Marcos",
        cliente_email="gabrielmmarcos@gmail.com",
        tipo_solicitacao="entrado",
        valor_patrimonio="1100",
    )
    # adiciona o cliente criado no banco
    session.add(new_cliente)
    await session.commit()
    # busca cliente no banco que tenha o nome Gabriel Marcos
    cliente = await session.scalar(
        select(Cliente).where(Cliente.cliente_nome == "Gabriel Marcos")
    )
    # verifica se esse cliente tem os dados do discionario
    assert asdict(cliente) == {
        "id": 1,
        "cliente_nome": "Gabriel Marcos",
        "cliente_email": "gabrielmmarcos@gmail.com",
        "tipo_solicitacao": "entrado",
        "valor_patrimonio": "1100",
        "status": StatusEnum.AGUARDANDO_ANALISE,
        "prioridade": None,
    }
