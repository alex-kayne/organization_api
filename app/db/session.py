from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/organization_api")

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
