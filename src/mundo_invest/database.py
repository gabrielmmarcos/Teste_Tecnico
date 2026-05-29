from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mundo_invest.settings import Settings

# criando engine do banco de dados
engine = create_async_engine(Settings().DATABASE_URL)


# usando engine como session
async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
