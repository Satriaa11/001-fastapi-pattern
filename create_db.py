import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.infrastructure.database import ASYNC_DATABASE_URL
from app.infrastructure.models import Base


async def create_tables():
    """Create database tables"""
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
