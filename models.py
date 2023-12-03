from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, Integer


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '99113322vfrcbv')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'asyncio')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)



class Base(DeclarativeBase, AsyncAttrs):
    pass


class Swapi(Base):
    __tablename__ = 'swapi'

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


