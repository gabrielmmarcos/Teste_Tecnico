import asyncio
from http import HTTPStatus
from sys import platform

from fastapi import FastAPI

from mundo_invest.routers.cliente_router import router
from mundo_invest.routers.webhook_router import webhook_router
from mundo_invest.schemas.root_schemas import Message

# forca o windows usar o asycio event loop
if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(
    title="Mundo Invest - Internal Management API",
    version="1.0.0",
    description="""Sistema interno para gerenciamento de clientes,
              controle de patrimônio investido e mapeamento
              de processos.""",
)

# rotas da api
app.include_router(router)
app.include_router(webhook_router)


# endpoint root
@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    # menssagem de boas vindas
    return {"message": "Teste técnico Mundo Invest!"}
