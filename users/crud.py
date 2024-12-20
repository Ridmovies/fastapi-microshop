from fastapi import HTTPException

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.models import User
from users.schemas import CreateUser


async def get_all_users(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(session: AsyncSession, user: CreateUser) -> User:
    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
