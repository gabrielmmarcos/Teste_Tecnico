import asyncio
import sys

import pytest
import pytest_asyncio

# forca o windows usar o asycio event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from mundo_invest.app import app
from mundo_invest.database import get_session
from mundo_invest.models.models import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # cria um cliente para simular requisicoes
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    # limpa para nao atrapalhar os outros dados
    app.dependency_overrides.clear()


# configuracao do banco de dados com docker
@pytest.fixture(scope="session")
def engine():
    # sobe o banco de dados como que vai ser usado como postgres
    with PostgresContainer("postgres:17", driver="psycopg") as postgres:
        # cria a engine
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    # cria todas as tabelas do banco
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    # abre a sessão no banco que vai ser usado como session
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    # drop o banco da memoria
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


# teste para verificar o tempo
# @contextmanager
# def _mock_db_time(*, model, time=datetime(2025, 9, 7)):
#     def fake_time_hook(mapper, connection, target: Produto):
#         if hasattr(target, "created_at") and hasattr(target, "updated_at"):
#             target.created_at = time
#             target.updated_at = time

#     event.listen(model, "before_insert", fake_time_hook)

#     yield time

#     event.remove(model, "before_insert", fake_time_hook)


# @pytest.fixture
# def mock_db_time():
#     return _mock_db_time
