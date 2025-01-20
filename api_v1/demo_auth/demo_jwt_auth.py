from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status)
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from pydantic import BaseModel

from api_v1.demo_auth.utils import (
    create_refresh_token,
    create_access_token,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
)
from users.schemas import UserSchema
from auth import utils_jwt as auth_utils

http_bearer = HTTPBearer(auto_error=False)
oath2_password_bearer = OAuth2PasswordBearer(tokenUrl="/jwt/login/")


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
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
    refresh_token: str | None = None
    token_type: str = "Bearer"


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
):
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/users/me/", response_model=UserSchema)
def get_current_user(user: UserSchema = Depends(get_current_user)):
    return user


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
