from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session