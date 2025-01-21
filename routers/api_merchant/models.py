from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from routers.admin.controller import get_user_from_api_key


class GetApiKey:
    async def __call__(self, request: Request):
        response = await get_user_from_api_key(request.headers.get('x-api-key'))
        if not response['Success']:
            raise HTTPException(
                status_code=404,
                detail="Не авторизован или сессия просрочена"
            )
        return response


class Invoice(BaseModel):
    __table_name__ = "pay_invoice"
    id: int | None = None
    req_id: int | None = None
    sum_fiat: float | None = None
    api_key: str | None = None


class Settings(BaseModel):
    __table_name__ = "pay_notify_user_settings"
    id: int | None = None
    user_id: int | None = None
    site_url: str | None = None
    success_url: str | None = None
    fail_url: str | None = None
    secret_word: str | None = None


class Shops(BaseModel):
    __table_name__ = "pay_shops"
    id: int | None = None
    uuid: str | None = None
    user_id: int | None = None
    title: str | None = None
    balance: float | None = None
    date: str | None = None

