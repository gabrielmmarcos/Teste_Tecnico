from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.models.models import Cliente
from mundo_invest.schemas.cliente_schemas import ClientePublic
from mundo_invest.schemas.root_schemas import FilterPage
# from mundo_invest.pipefy_client.pipefy import create_pipefy_card_mutation


# funcao que lista todos os clientes
async def read_all_clients_service(session: AsyncSession, filter: FilterPage):
    # select no banco de dados com o filter que vem do endpoint
    result = await session.scalars(
        select(Cliente).offset(filter.offset).limit(filter.limit)
    )

    return result.all()


# funcao que cria um usuario no banco de dados
async def create_client_service(
    client: ClientePublic, session: AsyncSession, is_batch=False
):
    # verifica se o email já existe
    db_client = await session.scalar(
        select(Cliente).where(
            and_(Cliente.cliente_email == client.cliente_email)
        )
    )

    if db_client:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Cliente Já Existe! Tente Cadastrar outro email.",
        )

    # cria a instância do cliente com os dados recebidos
    db_client = Cliente(
        cliente_nome=client.cliente_nome,
        cliente_email=client.cliente_email,
        tipo_solicitacao=client.tipo_solicitacao,
        valor_patrimonio=client.valor_patrimonio,
    )
    # adiciona o cliente na sessão do banco
    session.add(db_client)
    # salva as alterações no banco de dados
    await session.commit()
    # atualiza os dados do objeto com as informações do banco
    await session.refresh(db_client)
    
    # payload estruturado para criação do card no Pipefy
    # pipefy_payload = create_pipefy_card_mutation(db_client)
    
    # retonar o cliente
    return db_client
