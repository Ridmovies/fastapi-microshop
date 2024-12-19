import os
from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from core.config import settings


# URL базы данных
DATABASE_URL: str = settings.db_url

# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
# DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/tweeter"

# объект engine представляет соединение с базой данных PostgreSQL
# echo=True включает вывод всех SQL-запросов, что полезно при отладке.
engine = create_async_engine(DATABASE_URL, echo=settings.db_echo)
# Объект async_session_maker является фабрикой для создания асинхронных сессий.
# Параметр expire_on_commit=False указывает, что объекты, загруженные в сессию,
# не должны автоматически обновляться после каждого транзакционного блока
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Класс Base наследуется от DeclarativeBase
    и служит основой для определения моделей базы данных."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция get_session создает асинхронную сессию с базой данных
    и возвращает ее в виде итератора. Это позволяет использовать сессию
    в блоке async with, который гарантирует, что сессия будет закрыта после
    завершения блока кода."""
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    """Создание всех таблиц"""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
