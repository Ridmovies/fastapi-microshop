from fastapi import APIRouter, Request
from fastapi.params import Depends
from requests import session

from core.models.database import SessionDep
from core.models.models import User, Profile
from users import crud
from users.dependencies import GetUserDep
from users.schemas import (
    CreateUser,
    UserOutSchema,
    UserUpdateSchema,
    ProfileInSchema,
    ProfileOutSchema,
)

router = APIRouter()


@router.get("/", response_model=list[UserOutSchema])
async def get_users(session: SessionDep):
    return await crud.get_all_users(session=session)


@router.post("/", response_model=UserOutSchema)
async def create_user(session: SessionDep, user: CreateUser):
    return await crud.create_user(session=session, user=user)


@router.get("/id/{user_id}", response_model=UserOutSchema)
async def get_user(user: GetUserDep):
    return user


@router.get("/username/{username}", response_model=UserOutSchema)
async def get_user_by_username(session: SessionDep, username: str):
    return await crud.get_user_by_username(session=session, username=username)


@router.delete("/{user_id}")
async def delete_user(session: SessionDep, user: GetUserDep) -> None:
    await crud.delete_user(session=session, user=user)


@router.put("/{user_id}")
async def update_user(
    session: SessionDep, user: GetUserDep, new_data: UserUpdateSchema
):
    return await crud.update_user(session=session, user=user, new_data=new_data)


@router.post("/profile/{user_id}", response_model=ProfileOutSchema)
async def create_user_profile(
    session: SessionDep, user_id: int, profile: ProfileInSchema
):
    return await crud.create_user_profile(
        session=session, user_id=user_id, profile=profile
    )


# @router.get("/profile/{user_id}", response_model=ProfileOutSchema)
# async def get_user_with_profile(session: SessionDep, user_id: int):
#     return await crud.get_user_with_profile(session=session, user_id=user_id)
