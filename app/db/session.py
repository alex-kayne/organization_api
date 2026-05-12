from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
