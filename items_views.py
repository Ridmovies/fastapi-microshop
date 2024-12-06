from typing import Annotated, Union

from fastapi import Path, APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/items", tags=["items"])


class CreateUser(BaseModel):
    email: EmailStr


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/{item_id}/")
def read_item(item_id: Annotated[int, Path(ge=0, lt=100)], q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.post("/email/")
def send_email(user: CreateUser):
    return {"email": user.email}
