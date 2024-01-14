from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_async_session_maker(db_uri: str) -> async_sessionmaker:
    engine = create_async_engine(
        db_uri,
    )
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


async def get_async_session(async_session_maker: async_sessionmaker):
    async with async_session_maker() as session:
        yield session
