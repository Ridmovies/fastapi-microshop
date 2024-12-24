from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    # email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class UserOutSchema(BaseModel):
    id: int
    username: Annotated[str, MinLen(3), MaxLen(20)]


class UserUpdateSchema(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class ProfileInSchema(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    bio: str | None = None
    user_id: int


class ProfileOutSchema(ProfileInSchema):
    id: int
