from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from pydantic import BaseModel

from users.schemas import UserSchema
from auth import utils_jwt as auth_utils

# http_bearer = HTTPBearer(auto_error=False)
oath2_password_bearer = OAuth2PasswordBearer(tokenUrl="/jwt/login/")


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    # dependencies=[Depends(http_bearer)],
)


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("qwerty"),
)


users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


class TokenInfo(BaseModel):
    access_token: str
    # refresh_token: str | None = None
    token_type: str


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exp
    if auth_utils.validate_password(password=password, hashed_password=user.password):
        return user
    raise unauthed_exp


def get_current_token_payload(
    token: str = Depends(oath2_password_bearer),
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")


@router.get("/users/me/", response_model=UserSchema)
def get_current_user(user: UserSchema = Depends(get_current_user)):
    return user
