from fastapi import APIRouter

from users import crud
from users.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/email/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
