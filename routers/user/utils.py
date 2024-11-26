import json
import secrets
import string
import requests
#from passlib.context import CryptContext
import uuid
import sys
from datetime import timedelta, datetime, timezone
#from jose import jwt, JWTError
from fastapi import Response
import routers.user.models as user_models
import config
#from models import User, TokenPair, JwtTokenSchema
from typing import Any
from fastapi import HTTPException, status
REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail if detail else "Bad request",
        )


class AuthFailedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticate failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def hash_from_yii2(password):
    """
    получить хешкод пароля из yii2
    :param password:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/get-password'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'password': password  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


async def create_random_key(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(secrets.choice(chars) for _ in range(length))



#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


def _get_utc_now():
    if sys.version_info >= (3, 2):
        # For Python 3.2 and later
        current_utc_time = datetime.now(timezone.utc)
    else:
        # For older versions of Python
        current_utc_time = datetime.utcnow()
    return current_utc_time


# def _create_access_token(payload: dict, minutes: int | None = None) -> user_models.JwtTokenSchema:
#     expire = _get_utc_now() + timedelta(
#         minutes=minutes or config.ACCESS_TOKEN_EXPIRES_MINUTES
#     )
#     print(expire)
#     payload[EXP] = expire
#
#     token = user_models.JwtTokenSchema(
#         token=jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM),
#         payload=payload,
#         expire=expire,
#     )
#
#     return token


# def _create_refresh_token(payload: dict) -> user_models.JwtTokenSchema:
#     expire = _get_utc_now() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRES_MINUTES)
#
#     payload[EXP] = expire
#
#     token = user_models.JwtTokenSchema(
#         token=jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM),
#         expire=expire,
#         payload=payload,
#     )
#
#     return token


# def create_token_pair(user) -> user_models.TokenPair:
#     payload = {SUB: str(user), IAT: _get_utc_now()}
#
#     return user_models.TokenPair(
#         access=_create_access_token(payload={**payload}),
#         refresh=_create_refresh_token(payload={**payload}),
#     )


# def refresh_token_state(token: str):
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
#     except JWTError as ex:
#         print(str(ex))
#         raise AuthFailedException()
#
#     return {"token": _create_access_token(payload=payload).token}


# def mail_token(user: user_models.User):
#     """Return 2 hour lifetime access_token"""
#     payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT: _get_utc_now()}
#     return _create_access_token(payload=payload, minutes=2 * 60).token


def add_refresh_token_cookie(response: Response, token: str):
    exp = _get_utc_now() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRES_MINUTES)
    exp.replace(tzinfo=timezone.utc)

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )