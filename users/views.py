from fastapi import APIRouter
from fastapi.params import Depends

from core.models.database import SessionDep
from core.models.models import User
from users import crud
from users.dependencies import GetUserDep
from users.schemas import CreateUser, UserOutSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOutSchema])
async def get_users(session: SessionDep):
    return await crud.get_all_users(session=session)


@router.post("/", response_model=UserOutSchema)
async def create_user(session: SessionDep, user: CreateUser):
    return await crud.create_user(session=session, user=user)


@router.get("/{user_id}", response_model=UserOutSchema)
async def get_user(user: GetUserDep):
    return user


@router.delete("/{user_id}")
async def delete_user(session: SessionDep, user: GetUserDep) -> None:
    await crud.delete_user(session=session, user=user)
