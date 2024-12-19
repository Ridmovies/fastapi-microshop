from fastapi import APIRouter

from core.models.database import SessionDep
from core.models.models import User
from users import crud
from users.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/", response_model=list[User])
# async def get_users(session: SessionDep):
#     return await crud.get_all_users(session=session)
