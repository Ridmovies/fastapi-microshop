from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.models import User
from users.schemas import CreateUser


async def get_all_users(session: AsyncSession):
    query = select(User)
    result: Result = await session.execute(query)
    users = result.scalars().all()
    return list(users)
