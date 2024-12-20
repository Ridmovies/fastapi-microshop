from typing import Annotated

from fastapi import HTTPException, Path
from fastapi.params import Depends
from sqlalchemy import select, Result

from core.models.database import SessionDep
from core.models.models import User


async def get_user_by_id(session: SessionDep, user_id=Annotated[int, Path]) -> User:
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


GetUserDep = Annotated[User, Depends(get_user_by_id)]
