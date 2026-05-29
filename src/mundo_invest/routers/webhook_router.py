from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from mundo_invest.database import get_session
from mundo_invest.schemas.cliente_schemas import ClientePrioridade
from mundo_invest.schemas.root_schemas import FilterPage
from mundo_invest.schemas.webhook_schemas import WebhookList, WebhookResponse
from mundo_invest.services.webhook_services import (
    create_webhook_service,
    read_all_webhooks_service,
)

webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])

T_Session = Annotated[AsyncSession, Depends(get_session)]


# endpoint get listando todos os webhooks do banco
@webhook_router.get("/all", response_model=WebhookList)
async def read_all_webhooks(
    session: T_Session, filter: Annotated[FilterPage, Query()]
):
    return {"webhooks": await read_all_webhooks_service(session, filter)}


# endpoint post
@webhook_router.post("/pipefy/card-updated", response_model=ClientePrioridade)
async def create_webhook(
    webhook: WebhookResponse,
    session: T_Session,
):
    return await create_webhook_service(webhook, session)
