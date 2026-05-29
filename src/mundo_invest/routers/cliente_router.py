from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

# # teste
# from src.mundo_invest.database import get_session
# from src.mundo_invest.schemas.cliente_schemas import (
#     ClienteList,
#     ClientePublic,
#     ClienteResponse,
# )
# from src.mundo_invest.schemas.root_schemas import FilterPage
# from src.mundo_invest.services.cliente_services import (
#     create_client_service,
#     read_all_clients_service,
# )
from mundo_invest.database import get_session
from mundo_invest.schemas.cliente_schemas import (
    ClienteList,
    ClientePublic,
    ClienteResponse,
)
from mundo_invest.schemas.root_schemas import FilterPage
from mundo_invest.services.cliente_services import (
    create_client_service,
    read_all_clients_service,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])

T_Session = Annotated[AsyncSession, Depends(get_session)]


# endpoint get listando todos os clientes do banco
@router.get(
    "/all", response_model=ClienteList, response_model_exclude_none=True
)
async def read_all_clients(
    session: T_Session, filter: Annotated[FilterPage, Query()]
):
    return {"clientes": await read_all_clients_service(session, filter)}


# endpoint post para criar cliente
@router.post(
    "/criar_cliente",
    response_model=ClienteResponse,
    response_model_exclude_none=True,
)
async def create_client(
    client: ClientePublic,
    session: T_Session,
):
    return await create_client_service(client, session)
