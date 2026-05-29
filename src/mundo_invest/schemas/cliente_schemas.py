from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from mundo_invest.enums.enums import PrioridadeEnum, StatusEnum


# schemas para o endpoint post
class ClientePublic(BaseModel):
    # id: int
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float


# schemas para a resposta do endpoint post
class ClienteResponse(ClientePublic):
    status: StatusEnum = Field(default=StatusEnum.AGUARDANDO_ANALISE)
    prioridade: Optional[PrioridadeEnum] = None


# schemas para o endpoint get
class ClienteList(BaseModel):
    clientes: list[ClienteResponse]


# schemmas para post webhook
class ClientePrioridade(ClienteResponse):
    prioridade: str
