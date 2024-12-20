from fastapi import HTTPException
from requests import session

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from tomlkit import value

from core.models.models import User, Profile
from users.schemas import CreateUser, UserUpdateSchema, ProfileInSchema


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


async def update_user(
    session: AsyncSession, user: User, new_data: UserUpdateSchema
) -> User:
    for key, value in new_data.model_dump().items():
        setattr(user, key, value)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


async def create_user_profile(
    session: AsyncSession, user_id: int, profile: ProfileInSchema
) -> Profile:
    new_profile = Profile(**profile.model_dump())
    session.add(new_profile)
    await session.commit()
    return new_profile


async def get_user_with_profile(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id).options(joinedload(User.profile))
    user: User | None = await session.scalar(stmt)
    print(f"{user.profile=}")

    return {"user": user, "profile": user.profile}
